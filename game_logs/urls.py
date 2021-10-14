"""Defines URL patterns for game_logs"""

from django.urls import path
from . import views
from .views import GameDemoListView, GameDetailCreateView


app_name = "game_logs"

urlpatterns = [
    # Home page
    path("", GameDemoListView.as_view(), name="homepage"),
    path("about/", views.about, name="about"),
    path("game-detail/<int:pk>/", GameDetailCreateView.as_view(), name="game-detail"),
]
