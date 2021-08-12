from django.contrib import admin
from django.urls import path
from .views import StudyList, StudyCreate, StudyDelete, StudyUpdate

urlpatterns = [
    path("list/", StudyList.as_view(), name="list"),
    path("create/", StudyCreate.as_view(), name="create"),
    path("delete/<int:pk>", StudyDelete.as_view(), name="delete"),
    path("update/<int:pk>", StudyUpdate.as_view(), name="update"),
]
