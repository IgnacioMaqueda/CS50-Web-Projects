
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("poster/<str:name>", views.poster, name="poster"),
    path("following", views.following, name="following"),
    path("save/<int:post_id>", views.save, name="save"),
    path("like/<int:post_id>", views.like, name="like")
]
