from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create, name = "create"),
    path("profile/<str:username>", views.profile, name = "profile"),
    path("like", views.like, name = "like"),
    path("edits/<int:id>",views.edit, name = "edit"),
    path("following" , views.following , name= "following")
]
