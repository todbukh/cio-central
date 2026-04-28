# Project-wide middleware for inspecting user approval status on every request.
#
# Middleware runs before every view, use it for rules that
# should apply across the entire site (e.g. "banned users can never proceed").
# For more specific, per-view rules use the decorators in core/decorators.py instead.

from django.shortcuts import render, redirect
from core.permissions import is_approved, is_pending, is_rejected, is_banned


class ApprovalStatusMiddleware:

    # Paths matched by its prefix - bypassed entirely regardless of user status.
    # Basically, these are all the URL prefixes that need to be accessible regardless of approval status.
    EXEMPT_PATHS = [
        "/accounts/",       # allauth login, logout, signup routes
        "/admin/",          # Django admin
        "/admin",
        "/executive/roster/restore-application/"
    ]

    # Paths matched exactly.
    EXEMPT_EXACT_PATHS = [
        "/login/"          # core:login
    ]

    # Middleware owns these paths entirely - no URL patterns or views needed.
    # Maps path → template. Used both to serve the page and as redirect targets.
    STATUS_PAGES = {
        "/pending/":  "organization/pending.html",
        "/rejected/": "organization/rejected.html",
        "/banned/":   "organization/banned.html",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if self._is_exempt(request.path):
            return self.get_response(request)

        # added to handle redirecting the user admin away from most other pages
        if request.user.is_user_admin():
            if not request.path.startswith("/user-admin/") and not request.path.startswith("/admin"):
                return redirect("user_admin:user_admin")
            # short-circuit middleware here because status checks don't apply to USERADMINs
            return self.get_response(request)

        status_path = self._status_path(request.user)
        if status_path is not None:
            # Render if already on the correct status page, otherwise redirect.
            if request.path == status_path:
                return render(request, self.STATUS_PAGES[status_path])
            return redirect(status_path)

        # User is approved — if they're on a status page (e.g. refreshed after
        # being approved), send them to the home page since no view owns those paths.
        if request.path in self.STATUS_PAGES:
            return redirect("organization:home")

        return self.get_response(request)

    # --- helper functions ---

    # handles exempt paths that should bypass middleware
    def _is_exempt(self, path):
        if path in self.EXEMPT_EXACT_PATHS:
            return True
        return any(path.startswith(prefix) for prefix in self.EXEMPT_PATHS)

    # returns the redirect path based on user status, or None if no redirect is needed
    def _status_path(self, user):
        if is_approved(user):
            return None
        if is_pending(user):
            return "/pending/"
        if is_rejected(user):
            return "/rejected/"
        if is_banned(user):
            return "/banned/"
        return "/pending/"  # invalid status, treat as pending just in case
