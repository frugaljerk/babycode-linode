"""Defines URL patterns for order_codes"""

from django.urls import path
from game_logs.views import GameDetailCreateView
from game_logs.models import GameDemo
from . import views
from .models import MyBabyCodes


urlpatterns = [
    # path('game-detail/<int:pk>/', GameDetailCreateView.as_view(), name='game-detail'),
]
