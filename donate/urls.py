from django.urls import path
from . import views


app_name = "donate"

urlpatterns = [
    path("", views.index, name="index"),
    path("charge/", views.charge, name="charge"),
    path("success/<str:args>/", views.successMsg, name="success"),
    path(
        "machinecode/<int:pk>/",
        views.MachineCodeDonateView.as_view(),
        name="machinecode",
    ),
    path("humancode/<int:pk>/", views.HumanCodeDonateView.as_view(), name="humancode"),
]
