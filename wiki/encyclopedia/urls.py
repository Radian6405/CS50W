from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("wiki/<str:name>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("edit", views.edit, name="edit"),
    path("save", views.save, name="save"),
    path("random", views.randomPage, name="random")
]
