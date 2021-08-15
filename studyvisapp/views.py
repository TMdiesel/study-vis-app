import datetime
from datetime import timedelta

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
import jpholiday

from .models import TimeModel
from .forms import HomeForm

# Create your views here.
class StudyList(ListView):
    template_name = "list.html"
    model = TimeModel
    paginate_by = 100
    queryset = model.objects.order_by("-starttime")

    def get_queryset(self):
        if self.request.GET.get("yearmonth") is None:
            year = datetime.date.today().year
            month = datetime.date.today().month
        else:
            year = self.request.GET.get("yearmonth").split("-")[0]
            month = self.request.GET.get("yearmonth").split("-")[1]

        object_list = self.model.objects.filter(
            starttime__year=year, starttime__month=month
        ).order_by("-starttime")
        return object_list


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
        # specify the date range
        if self.request.GET.get("yearmonth") is None:
            year = datetime.date.today().year
            month = datetime.date.today().month
        else:
            year = self.request.GET.get("yearmonth").split("-")[0]
            month = self.request.GET.get("yearmonth").split("-")[1]

        # read&create data
        df = pd.DataFrame(
            list(
                TimeModel.objects.filter(
                    starttime__year=year, starttime__month=month
                ).values()
            )
        )
        df["duration"] = df["duration"].apply(lambda x: x.total_seconds() / 3600)
        df["date"] = df["starttime"].apply(lambda x: x.date())
        date_df = df.groupby("date").sum()[["duration"]]
        date_df = self._complement_date(date_df)
        task_num_gdf = df.groupby("item").sum()[["duration"]]
        _, holiday_index = self._create_biz_hol_index(
            date_df.index.min(), date_df.index.max()
        )

        # create graph
        fig1 = go.Figure(
            go.Scatter(
                x=date_df.index,
                y=date_df["duration"].round(decimals=1),
                mode="lines+markers",
                marker=dict(
                    size=7,
                ),
                name="all",
            ),
            layout=go.Layout(
                title=f"勉強時間の推移({year}/{month})",
                width=800,
                height=400,
                xaxis=dict(
                    range=[
                        date_df.index.min() - timedelta(days=1),
                        date_df.index.max() + timedelta(days=1),
                    ],
                    dtick="D",
                    tickformat="%d",
                ),
            ),
        )
        fig1.add_trace(
            go.Scatter(
                x=date_df.index[holiday_index],
                y=date_df["duration"][holiday_index],
                mode="markers",
                marker=dict(
                    size=7,
                ),
                name="休日",
            ),
        )

        fig2 = go.Figure(
            go.Bar(
                x=task_num_gdf.index,
                y=task_num_gdf["duration"].round(decimals=1),
            ),
            layout=go.Layout(
                title=f"項目ごとの勉強時間({year}/{month})",
                width=800,
                height=400,
            ),
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

    def _create_biz_hol_index(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> pd.date_range:
        """
        平日と休日のindexを返す
        """

        year = start_date.year
        holiday = []
        holiday_dict = jpholiday.year_holidays(year)
        for i in range(len(holiday_dict)):
            holiday.append(holiday_dict[i][0])
        holiday = holiday + [
            datetime.date(year, 1, 1),
            datetime.date(year, 1, 2),
            datetime.date(year, 1, 3),
            datetime.date(year, 12, 31),
        ]  # 年末年始追加
        holiday = sorted(list(set(holiday)))  # for uniqueness
        holiday = pd.to_datetime(holiday)

        calendar_full = pd.date_range(start_date, end_date, freq="D")
        business_index = []
        holiday_index = []
        for idx, calendar in enumerate(calendar_full):
            if (
                (not calendar in holiday)
                and (calendar.weekday() >= 0)
                and (calendar.weekday() <= 4)
            ):
                business_index.append(idx)
            else:
                holiday_index.append(idx)

        return business_index, holiday_index
