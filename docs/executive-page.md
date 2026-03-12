# Executive Page & Role-Based Routing

## Overview

The app uses `role` and `status` fields on the User model. Executive access is granted to users with the `OWNER` or `EXEC` role. This is separate from Django's `is_staff` (which controls `/admin/` access).

## How It Works

1. **Login** — Users log in via Google OAuth (allauth).
2. **Status gating** — The home view checks `status` before rendering content:
   - `PENDING` → pending approval page
   - `REJECTED` → rejected page
   - `BANNED` → banned page
   - `APPROVED` → normal home page
3. **Access control** — The `/executive/` view is protected by `@login_required` and `@user_passes_test(is_exec)`. Non-exec users are redirected to `/`.
4. **Navigation** — The "Exec Panel" nav link in `base.html` is only rendered for authenticated exec users.

## Key Files

| File                                                  | Purpose                                                                                                                                                                       |
|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `core/models.py`                                      | `User` model with `Role` and `Status` choices                                                                                                                                 |
| `core/views.py`                                       | `home` (status-gated) and `login` views                                                                                                                                       |
| `exec_panel/views.py`                                 | `executive_redirect` and `executive` (status-gated) - the first redirects to `/executive/roster/` and the second is of the form `/executive/<str:tab>/`                       |
| `core/urls.py`                                        | Routes for `/` and `/login/`                                                                                                                                                  |
| `exec_panel/urls.py`                                  | Routes for `/executive/` and `/executive/<str:tab>/`                                                                                                                          |
| `exec_panel/templates/exec_panel/executive-base.html` | Base executive page template. The individual executive tab pages will extend this in order for all of them to have the same tab nav bar                                       |
| `exec_panel/templates/exec_panel/tabname.html`        | Each of these is the template for the focused tab. They each extend `executive-base.html`. They include `roster.html`, `attendance.html`, `analytics.html`, and `events.html` |
| `templates/base.html`                                 | Conditional "Exec Panel" nav link                                                                                                                                             |

## Assigning Roles

Use the Django admin panel at `/admin/` → Users → select user → set **Role** and **Status** fields.

## Deep Linking

Because the login flow preserves the incoming `next` destination, deep linking is preserved. If a user visits a protected page while logged out, they'll be returned to that page after login instead of being forced to the default landing page.
