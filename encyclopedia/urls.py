from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.content, name="content"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create")
]
