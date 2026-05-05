import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Movie, Room
from .forms import RegisterForm

API_KEY = settings.TMDB_API_KEY


# ----------- AUTH -----------

def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")

    return render(request, "films/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "films/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


# ----------- DASHBOARD -----------

@login_required
def dashboard(request):
    rooms = Room.objects.filter(owner=request.user)
    return render(request, "films/dashboard.html", {"rooms": rooms})


# ----------- ROOM -----------

@login_required
def create_room(request):
    if request.method == "POST":
        name = request.POST.get("name")
        room = Room.objects.create(name=name, owner=request.user)
        return redirect("room", room.code)

    return render(request, "films/create_room.html")


@login_required
def join_room(request):
    if request.method == "POST":
        code = request.POST.get("code")
        return redirect("room", code)

    return render(request, "films/join_room.html")


@login_required
def room_view(request, code):
    room = Room.objects.get(code=code)
    movies = Movie.objects.filter(room=room)

    return render(request, "films/room.html", {
        "room": room,
        "movies": movies
    })


# ----------- MOVIES -----------

@login_required
def add_movie(request, code):
    if request.method == "POST":
        title = request.POST.get("title")
        room = Room.objects.get(code=code)
        Movie.objects.create(title=title, room=room)
    return redirect("room", code)


@login_required
def toggle_watched(request, movie_id, code):
    movie = Movie.objects.get(id=movie_id)
    movie.watched = not movie.watched
    movie.save()
    return redirect("room", code)


@login_required
def update_description(request, movie_id, code):
    if request.method == "POST":
        movie = Movie.objects.get(id=movie_id)
        movie.description = request.POST.get("description")
        movie.save()
    return redirect("room", code)


# ----------- SEARCH -----------

@login_required
def search(request, code):
    query = request.GET.get("q")

    movies = []
    if query:
        url = "https://api.themoviedb.org/3/search/multi"
        params = {
            "api_key": API_KEY,
            "query": query,
        }
        response = requests.get(url, params=params)
        data = response.json()

        for item in data.get("results", []):
            title = item.get("title") or item.get("name") or "Без названия"
            movies.append({"title": title})

    return render(request, "films/search.html", {
        "movies": movies,
        "code": code
    })