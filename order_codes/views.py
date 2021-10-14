from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyBabyCodes, GameDemo
from .forms import OrderForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
