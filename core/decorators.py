# View level access control decorators.
#
# Apply these directly to the individual views across any app in the project.
# Works alongside the project-wide middleware in core/middleware.py. Middleware
# runs on every request, while these decorators enforce more narrow rules on
# specific views only.
#
# Usage example:
#   from core.decorators import approved_required, executive_required
#
#   @approved_required
#   def my_view(request):
#       ...

import functools
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import NoReverseMatch, reverse
from core.permissions import is_approved, is_executive

# NOTE: Just a reminder that approval status is checked globally in core/middleware.py

# Checks for approved executives or owners.
# Raises PermissionDenied (HTTP 403) by default, or redirects to redirect_url if provided.
#
# Usage:
#   @executive_required                                     # raises 403 (PermissionDenied)
#   @executive_required(redirect_url="organization:home")   # redirects to named URL
def executive_required(view_func=None, *, redirect_url=None):
    def decorator(func):
        # using functools.wraps to preserve original function's metadata (e.g. name, docstring) in the wrapper
        # don't totally understand why this is necessary but it's a common best practice for decorators so we'll do it just in case
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if not is_executive(request.user):
                if redirect_url:
                    try:
                        # First, treat redirect_url as a URL name for reverse().
                        return redirect(reverse(redirect_url))
                    except NoReverseMatch:
                        # If reversing fails, fall back to using redirect_url as a literal URL/path.
                        return redirect(redirect_url)
                raise PermissionDenied
            return func(request, *args, **kwargs) # call original view function if check passes 
        return wrapper

    # allows use as @executive_required (no parentheses) or @executive_required(redirect_url="...")
    if view_func is not None:
        return decorator(view_func)
    return decorator

# Add more decorators down here as needed
