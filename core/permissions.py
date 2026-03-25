# Reusable, stateless permission helpers for the project.
#
# These are plain functions that accept a User object and return a boolean.
# They do NOT handle redirects, raise exceptions, or touch the request object —
# that responsibility belongs to middleware (core/middleware.py) and decorators
# (core/decorators.py), both of which import from here.
#
# Usage example:
#   from core.permissions import is_approved
#   if is_approved(request.user):
#       ...

# Return True if the user is logged in (not anonymous).
# For now I think we can stick to using Django's built-in is_authenticated, but this function is here if we want to add any extra logic to it down the line.
def is_authenticated_user(user):
    return bool(user and user.is_authenticated)

# For all the following, is_authenticated_user(user) is checked first to avoid potentially
# attempting to access unset fields on an anonymous user
# Credit to Copilot for pointing out this lack of defensive programming

# Return True if the user's status is APPROVED.
def is_approved(user):
    return is_authenticated_user(user) and user.status == user.Status.APPROVED

# Return True if the user's status is PENDING (awaiting approval).
def is_pending(user):
    return is_authenticated_user(user) and user.status == user.Status.PENDING

# Return True if the user's status is REJECTED.
def is_rejected(user):
    return is_authenticated_user(user) and user.status == user.Status.REJECTED

# Return True if the user's status is BANNED.
def is_banned(user):
    return is_authenticated_user(user) and user.status == user.Status.BANNED

# Return True if the user holds an executive-level role (EXEC or OWNER).
# This is the single source of truth for executive access logic.
def is_executive(user):
    return is_authenticated_user(user) and user.role in {user.Role.OWNER, user.Role.EXEC}

def is_owner(user):
    return is_authenticated_user(user) and user.role == user.Role.OWNER

# Add more helper functions here down the line as needed.
