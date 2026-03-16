# core/middleware.py
#
# Project-wide middleware for inspecting user approval status on every request.
#
# Middleware runs before every view, use it for rules that
# should apply across the entire site (e.g. "banned users can never proceed").
# For more specific, per-view rules use the decorators in core/decorators.py instead.
#
# HOW TO WIRE THIS IN (when you're ready):
#   In settings.py, add to MIDDLEWARE (after AuthenticationMiddleware):
#       'core.middleware.ApprovalStatusMiddleware',

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from core.permissions import is_approved, is_banned, is_pending, is_rejected

# Redirects authenticated users to core:home based on their approval status.
# core/views.py home() already renders the appropriate template (pending.html,
# rejected.html, banned.html) so all three statuses share the same redirect target.
class ApprovalStatusMiddleware(MiddlewareMixin):

    # Paths matched by its prefix - bypassed entirely regardless of user status.
    # Critical for avoiding redirect loops and keeping auth flows accessible.
    EXEMPT_PATHS = [
        "/accounts/",       # allauth login, logout, signup routes
        "/admin/",          # Django admin
    ]

    # Paths matched exactly — home is exempt because it renders the status
    # pages itself; exempting it prevents an infinite redirect loop.
    EXEMPT_EXACT_PATHS = [
        "/",                # core:home — handles pending/rejected/banned rendering
        "/login/",          # core:login
    ]

    def process_request(self, request):
        # Called before the view on every request.
        # Return None to let the request continue normally,
        # or return an HttpResponse (e.g. a redirect) to short-circuit the view.

        user = request.user

        # Skip anonymous (not logged-in) users entirely.
        # this should be handled by AuthenticationMiddleware
        # checking this here just in case to avoid any issues with missing user objects in the status checks below.
        if not user.is_authenticated:
            return None

        # Skip exempt paths so auth flows and status pages always work.
        if self._is_exempt(request.path):
            return None

        if is_banned(user):
            return redirect("core:home")

        if is_rejected(user):
            return redirect("core:home")

        if is_pending(user):
            return redirect("core:home")

        if is_approved(user):
            # This is the valid user state to gain access to most apps, so allow through.
            return None

        # Fallback: unknown status — allow through. Shouldn't happen
        return None

    # ---------------------------------------------------------------------- #
    # Private helpers                                                          #
    # ---------------------------------------------------------------------- #

    # Return true if the given path should bypass status checks
    def _is_exempt(self, path):
        if path in self.EXEMPT_EXACT_PATHS:
            return True
        return any(path.startswith(prefix) for prefix in self.EXEMPT_PATHS)
