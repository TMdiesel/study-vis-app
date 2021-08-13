import datetime

from django.shortcuts import render
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils.timezone import make_aware

from .models import TimeModel
from .forms import HomeForm

# Create your views here.
class StudyList(ListView):
    template_name = "list.html"
    model = TimeModel


class StudyCreate(CreateView):
    template_name = "create.html"
    model = TimeModel
    success_url = reverse_lazy("list")
    fields = ("item", "memo", "starttime", "endtime")


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
        object.starttime = make_aware(now)
        object.isactive = True
        object.save()
        return render(request, "list.html")


class StudyEnd(UpdateView):
    template_name = "end.html"
    model = TimeModel
    success_url = reverse_lazy("list")
    fields = ("item", "memo", "starttime", "endtime", "duration", "isactive")

    def post(self, request, pk):
        article = TimeModel.objects.get(pk=pk)
        form = HomeForm(request.POST, instance=article)
        now = datetime.datetime.now()
        object = form.save(commit=False)
        object.endtime = make_aware(now)
        object.isactive = False
        object.save()
        return render(request, "list.html")


def StudyTimer(request):
    return render(request, "timer.html")
