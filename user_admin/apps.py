from django.apps import AppConfig


class UserAdminConfig(AppConfig):
    name = "user_admin"

    def ready(self):
        import user_admin.signals
