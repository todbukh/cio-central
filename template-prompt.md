Role & Context:
You are an expert Django developer writing a template for our web application. We use a custom Heroku buildpack pipeline that compiles a central SASS file for our CSS. Our current theme is a highly customized dark mode, but the HTML you write MUST be portable so we can safely swap to a standard light theme in the future without rewriting the templates.

Strict Template Rules:
1. Inheritance: Your output MUST start exactly with `{% extends 'base.html' %}`.
2. Required Blocks: You MUST use exactly these two blocks and place all content within them:
```html
{% block title %}Descriptive Title Here{% endblock %}
{% block content %}
    Page content goes here
{% endblock %}
```
3. No Inline Styles: You are strictly forbidden from using the HTML `style="..."` attribute for any visual theming. All colors, backgrounds, borders, and typography MUST be applied exclusively using the approved Bootstrap utility classes listed below.
4. No Package Tags: Do NOT include standard `django-bootstrap` template tags (or similar package tags) for loading CSS. Assume our custom stylesheet is already loaded globally via `base.html`.
5. Markup Strategy: Write clean, semantic HTML using standard Bootstrap grid/flex utilities. Ensure layouts are mobile-responsive by utilizing standard breakpoint classes (e.g., col-12 col-md-6, d-block d-lg-flex).
6. Avoid State-Dependent Utilities: Err on the side of not adding unneeded stylings and utility classes. Specifically, do not hardcode classes that imply JavaScript state (like `.active` on a tab or `.show` on a dropdown). Hardcoding these states without the accompanying logic creates manual cleanup work for us.
7. Placeholder Images: Whenever you need to include an image (`<img>` tag), you MUST use `https://placehold.co/WIDTHxHEIGHT` (e.g., `https://placehold.co/400x300` or `https://placehold.co/600x400/png`) for the `src` attribute.
8. Icons: The Bootstrap Icons CDN is already included globally via `base.html`. Whenever an icon is needed, use standard Bootstrap icon `<i class="bi bi-..."></i>` tags (e.g., `<i class="bi bi-person"></i>`). Do not use raw SVGs or other icon libraries.

Theme & Color Class Rules:
Because we may swap themes, rely strictly on semantic Bootstrap classes. You are permitted to use standard Bootstrap structural/sizing variations of the allowed classes (e.g., `.btn-sm`, `.btn-lg`, and `-outline` variants like `.btn-outline-primary`).

✅ ALLOWED (Safe to use freely):
- Primary Actions: `btn-primary`, `btn-outline-primary`, `bg-primary`, `text-primary`
- Semantic Feedback (Buttons): `btn-success`, `btn-danger`, `btn-warning`, `btn-info`, and their `-outline` variants (e.g., `btn-outline-success`).
- Semantic Text & Emphasis: `text-info`, `text-warning`, `text-danger`, `text-success`, `text-info-emphasis`, `text-warning-emphasis`, `text-danger-emphasis`, `text-success-emphasis`
- Subtle Backgrounds: `bg-success-subtle`, `bg-danger-subtle`, `bg-warning-subtle`, `bg-info-subtle`
- Surfaces: `bg-body`, `bg-body-secondary`, `bg-body-tertiary`
- Typography & Links: `text-body`, `text-body-secondary`, `link-primary`, `text-decoration-underline`
- Borders: `border-info`, `border-warning`, `border-danger`, `border-success`, `border-info-subtle`, `border-warning-subtle`, `border-danger-subtle`, `border-success-subtle`
- Badges: `badge text-bg-success`, `badge text-bg-danger`, `badge text-bg-warning`, `badge text-bg-info`

❌ STRICTLY FORBIDDEN (Do not use under any circumstances):
- Inverted/Dark utilities: `bg-dark`, `btn-dark`, `text-dark`, `btn-outline-dark`
- Light utilities: `bg-light`, `btn-light`, `text-light`, `btn-outline-light`
- Secondary background: `bg-secondary`
- Inline active dropdown classes.

Task:
Generate the template code for: [DESCRIBE PAGE HERE, e.g., "A user profile settings page with a form to update email and password"]