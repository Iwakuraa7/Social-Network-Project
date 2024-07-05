import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post

@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        # If POST create new Post object
        content = request.POST["content"]
        Post.objects.create(content=content, author=request.user)

    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def user_view(request, username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        if request.POST.get("follow"):
            user.followers.add(request.user)
            user.save()

        elif request.POST.get("unfollow"):
            user.followers.remove(request.user)
            user.save()

    return render(request, "network/user-page.html", {
    "user": user,
    "users_posts": user.posts.order_by("-timestamp")
})

@login_required(login_url='login')
def following_view(request):
    user = User.objects.get(username=request.user.username)
    posts = []
    followed_users = user.following.all()
    for user in followed_users:
        for post in user.posts.order_by("-timestamp"):
            posts.append(post)

    return render(request, "network/following-page.html", {
        "posts": posts
    })
@csrf_exempt
def edit_post(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
            post.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid post id"})

@csrf_exempt
def like_post(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)
        if data.get("likes") is not None:
            for user in post.likes.all():
                if request.user == user:
                    post.likes.remove(user)
                    post.save()
                    return JsonResponse({"success": True, "like": False})
            else:
                post.likes.add(request.user)
                post.save()
                return JsonResponse({"success": True, "like": True})

    return JsonResponse({"success": False, "error": "Invalid post id"})
