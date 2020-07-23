import json
import requests
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User,Post,Profile,Like

#class to edit the from field
class Edit(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 1,'cols': 130, 'rows':10}), label='')


def index(request):
    posts = Post.objects.all().order_by('-time')
    p = Paginator(posts, 10)
    pnumber = request.GET.get('page')
    obj = p.get_page(pnumber)

    return render(request, "network/index.html",{"obj": obj})


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

#Creating New Post
@csrf_exempt
@login_required
def create(request):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        post = data.get("post")

        if len(post) == 0 or len(title) == 0 :
            return JsonResponse({"error": "One or more field is empty.", "status": 400}, status = 400)

        current_user = request.user
        likes = None
        #Add to database
        create_post = Post(user=current_user,title=title,post=post)
        create_post.save()

        return JsonResponse({"message": "Post Uploaded.", "status": 200}, status=200)


#Visit Users Profile
@csrf_exempt
@login_required
def profile(request,username):
    user = User.objects.get(username = username)
    posts = Post.objects.filter(user = user).order_by('-time')
    follower = Profile.objects.filter(following = user)
    following = Profile.objects.filter(follower = user)

    p = Paginator(posts, 10)
    pnumber = request.GET.get('page')
    obj = p.get_page(pnumber)

    if request.method == "GET":
        do = Profile.objects.filter(follower = request.user , following = user)
        return render(request,"network/profile.html",{"Puser": user,"obj":obj,"follower":follower,"following":following,"do":do})
    else:
        print("In Post Request")
        check = Profile.objects.filter(follower = request.user, following = user)
        if check:
            follo = Profile.objects.get(following = user,follower = request.user).delete()
        else:
            follo = Profile(following = user , follower = request.user)
            follo.save()

        follower = Profile.objects.filter(following = user)
        following = Profile.objects.filter(follower = user)
        do = Profile.objects.filter(follower = request.user , following = user)

    return render(request,"network/profile.html",{"Puser": user,"obj":obj,"follower":follower,"following":following,"do":do})



#user Press Like icon on site
@csrf_exempt
@login_required
def like(request):
    if request.method == 'GET':
        id = request.GET['id']
        post = Post.objects.get(pk=id)
        if request.user in post.liked.all():
            post.liked.remove(request.user)
            like = Like.objects.get(posts=post,user=request.user).delete()
        else:
            like = Like(posts=post,user=request.user)
            like.save()
            post.liked.add(request.user)
            post.save()
        return HttpResponse('Success')


#user requested to edit the post.
def edit(request,id):
    post = Post.objects.get(pk=id)
    if request.user == post.user:
        if request.method == "GET":
            return render(request, "network/edit.html", {"id":id,"edit":Edit(initial={"text": post.post})})

        else:
            form = Edit(request.POST)
            if form.is_valid():
                textarea = form.cleaned_data["text"]
                post.post = textarea
                post.save()
    return redirect('index')


#Follwing Page
def following(request):
    follo = Profile.objects.filter(follower = request.user)
    if not follo:
        return render(request,"network/following.html",{"message": "You have no followers!"})
    posts = Post.objects.all().order_by('-time')
    allposts = []

    for post in posts:
        for fol in follo:
            if fol.following == post.user:
                allposts.append(post)
    p = Paginator(allposts, 10)
    pnumber = request.GET.get('page')
    obj = p.get_page(pnumber)
    return render(request,"network/following.html",{"obj":obj})



#___END___
