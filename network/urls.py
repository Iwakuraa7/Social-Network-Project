
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_view, name="following"),
    path("<str:username>", views.user_view, name="user_page"),

    # API routes
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("like/<int:post_id>", views.like_post, name="like_post"),
]
