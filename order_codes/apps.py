from django.apps import AppConfig


class OrderCodesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order_codes"

    def ready(self):
        import order_codes.signals
