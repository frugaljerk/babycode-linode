from django.apps import AppConfig


class OrderDrawingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order_drawings"

    def ready(self):
        import order_drawings.signals
