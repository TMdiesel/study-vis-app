import datetime

from django.shortcuts import render
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import TimeModel
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from .forms import HomeForm

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
    success_url = reverse_lazy("list")
    fields = ("item",)

    def post(self, request):
        form = HomeForm(request.POST)
        now = datetime.datetime.now()
        object = form.save(commit=False)
        object.starttime = now.strftime("%Y-%m-%d %H:%M:%S")
        object.save()
        return render(request, "list.html")
