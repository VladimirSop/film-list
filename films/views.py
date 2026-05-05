import requests
from django.shortcuts import render, redirect
from .models import Movie
from django.conf import settings

API_KEY = settings.TMDB_API_KEY


def home(request):
    movies = Movie.objects.all()
    return render(request, "films/home.html", {"movies": movies})


def search(request):
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

        results = data.get("results", [])

        # 👇 ВАЖНО: нормализуем данные
        for item in results:
            title = item.get("title") or item.get("name") or "Без названия"
            movies.append({
                "title": title
            })

    return render(request, "films/search.html", {"movies": movies})


def add_movie(request):
    if request.method == "POST":
        title = request.POST.get("title")
        Movie.objects.create(title=title)
    return redirect("home")


def toggle_watched(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.watched = not movie.watched
    movie.save()
    return redirect("home")


def update_description(request, movie_id):
    if request.method == "POST":
        movie = Movie.objects.get(id=movie_id)
        movie.description = request.POST.get("description")
        movie.save()
    return redirect("home")