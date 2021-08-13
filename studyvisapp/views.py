from django.shortcuts import render

# Create your views here.
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import TimeModel
from django.urls import reverse_lazy

# Create your views here.
class StudyList(ListView):
    template_name = "list.html"
    model = TimeModel


class StudyCreate(CreateView):
    template_name = "create.html"
    model = TimeModel
    success_url = reverse_lazy("list")
    fields = ("item", "memo", "starttime", "endtime", "duration")


class StudyDelete(DeleteView):
    template_name = "delete.html"
    model = TimeModel
    success_url = reverse_lazy("list")


class StudyUpdate(UpdateView):
    template_name = "update.html"
    model = TimeModel
    success_url = reverse_lazy("list")
    fields = ("item", "memo", "starttime", "endtime", "duration")


class StudyHome(CreateView):
    template_name = "home.html"
    model = TimeModel
    success_url = reverse_lazy("home")
    fields = ("item",)
