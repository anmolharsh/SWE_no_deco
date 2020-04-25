from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
# from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView, View

