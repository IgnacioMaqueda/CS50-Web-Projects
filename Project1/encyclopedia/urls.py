from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("create/", views.create, name="create"),
    path("randompage/", views.randompage, name="randompage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("search/<str:title>", views.search, name="search")
]
