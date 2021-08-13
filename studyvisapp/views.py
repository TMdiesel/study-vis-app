import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
import plotly.graph_objects as go
import pandas as pd

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
        return redirect("list")


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
        return redirect("list")


def StudyTimer(request):
    return render(request, "timer.html")


class StudyVis(TemplateView):
    template_name = "vis.html"

    def get_context_data(self, **kwargs):
        context = super(StudyVis, self).get_context_data(**kwargs)
        context["plot1"], context["plot2"] = self._create_graph()
        return context

    def _create_graph(self):
        df = pd.DataFrame(list(TimeModel.objects.all().values()))
        df["duration"] = df["duration"].apply(lambda x: x.total_seconds() / 3600)
        df["date"] = df["starttime"].apply(lambda x: x.date())
        date_df = df.groupby("date").sum()[["duration"]]
        date_df = self._complement_date(date_df)
        task_num_gdf = df.groupby("item").sum()[["duration"]]

        fig1 = go.Figure(
            go.Scatter(
                x=date_df.index,
                y=date_df["duration"],
            ),
            layout=go.Layout(width=800, height=400),
        )
        fig2 = go.Figure(
            go.Bar(
                x=task_num_gdf.index,
                y=task_num_gdf["duration"],
            ),
            layout=go.Layout(width=800, height=400),
        )
        return fig1.to_html(include_plotlyjs=False), fig2.to_html(
            include_plotlyjs=False
        )

    def _complement_date(self, s: pd.Series) -> pd.DataFrame:
        """
        日付がindexのSeriesを入力して、
        欠けている日付をmin_dateからmax_dateの範囲で埋める
        """
        str_min_date = s.index.min().strftime("%Y-%m-%d")
        str_max_date = s.index.max().strftime("%Y-%m-%d")
        dates_df = pd.DataFrame(
            index=pd.date_range(str_min_date, str_max_date, freq="D")
        )
        return (
            pd.DataFrame(s)
            .merge(dates_df, how="outer", left_index=True, right_index=True)
            .fillna(0)
        )
