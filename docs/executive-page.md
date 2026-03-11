# Executive Page & Role-Based Routing

## Overview

The app uses `role` and `status` fields on the User model. Executive access is granted to users with the `OWNER` or `EXEC` role. This is separate from Django's `is_staff` (which controls `/admin/` access).

## How It Works

1. **Login** — Users log in via Google OAuth (allauth).
2. **Redirect** — A custom allauth adapter (`core/adapters.py`) checks the user's role:
   - `OWNER` or `EXEC` → redirected to `/executive/`
   - `MEMBER` → redirected to `/`
3. **Status gating** — The home view checks `status` before rendering content:
   - `PENDING` → pending approval page
   - `REJECTED` → rejected page
   - `BANNED` → banned page
   - `APPROVED` → normal home page
4. **Access control** — The `/executive/` view is protected by `@login_required` and `@user_passes_test(is_exec)`. Non-exec users are redirected to `/`.
5. **Navigation** — The "Exec Panel" nav link in `base.html` is only rendered for authenticated exec users.

## Key Files

| File | Purpose |
|------|---------|
| `core/models.py` | `User` model with `Role` and `Status` choices |
| `core/adapters.py` | Custom allauth adapter for role-based post-login redirect |
| `core/views.py` | `home` (status-gated), `executive_home`, `post_login_redirect`, `login` views |
| `core/urls.py` | Routes for `/`, `/login/`, `/post-login/`, `/executive/` |
| `core/templates/core/executive.html` | Executive landing page template |
| `templates/base.html` | Conditional "Exec Panel" nav link |
| `project_a_17/settings.py` | `ACCOUNT_ADAPTER` setting |

## Assigning Roles

Use the Django admin panel at `/admin/` → Users → select user → set **Role** and **Status** fields.

## Deep Linking

Because the login flow preserves the incoming `next` destination, deep linking is preserved. If a user visits a protected page while logged out, they'll be returned to that page after login instead of being forced to the default landing page.
