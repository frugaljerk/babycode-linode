from django.urls import path
from .views import OrderDrawingsCreateView

app_name = "order_drawings"

urlpatterns = [
    path("<int:pk>/", OrderDrawingsCreateView.as_view(), name="orderPage"),
]
