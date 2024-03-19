import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page = paginator.page(1)
    if request.method == "POST":
        post = Post(poster=request.user, content=request.POST["text"])
        post.save()
    elif "page" in request.GET:
        page = paginator.page(request.GET["page"])
    return render(request, "network/index.html", {
        "range": paginator.page_range,
        "page": page
    })


def save(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated."}, status=404)
    if request.method == "PUT":
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        if request.user != post.poster:
            return JsonResponse({"error": "You don't have permission."}, status=404)
        post.content = json.loads(request.body)["text"]
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=201)
    return JsonResponse({"error": "Invalid request."}, status=404)


def like(request, post_id):
    print("ARRANCO")
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated."}, status=404)
    if request.method == "PUT":
        print("ENTRO")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        liked = Like.objects.filter(user=request.user, post=post).exists()
        if not liked:
            post.likes += 1
            post.save()
            like = Like(user=request.user, post=post)
            like.save()
        return JsonResponse({"message": "Post liked successfully."}, status=201)
    return JsonResponse({"error": "Invalid request."}, status=404)


def following(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(poster__in=following_users).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page = paginator.page(1)
    if request.method == "POST":
        post = Post(poster=request.user, content=request.POST["text"])
        post.save()
    elif "page" in request.GET:
        page = paginator.page(request.GET["page"])
    page.object_list[0] = page.object_list[1]
    print(page.object_list[0])
    post_list = page
    return render(request, "network/following.html", {
        "range": paginator.page_range,
        "page": page
    })


def poster(request, name):
    poster = User.objects.get(username=name)
    posts = Post.objects.filter(poster=poster).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page = paginator.page(1)
    if request.method == "POST":
        if 'following' in request.POST:
            follow = Follow(follower=request.user, following=poster)
            follow.save()
        else:
            follow = Follow.objects.get(follower=request.user, following=poster)
            follow.delete()
    elif "page" in request.GET:
        page = paginator.page(request.GET["page"])
    followed = Follow.objects.filter(following=poster, follower=request.user).exists()
    following = Follow.objects.filter(follower=poster).count()
    followers = Follow.objects.filter(following=poster).count()
    return render(request, "network/poster.html", {
        "range": paginator.page_range,
        "page": page,
        "poster": poster,
        "following": following,
        "followers": followers,
        "followed": followed
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

