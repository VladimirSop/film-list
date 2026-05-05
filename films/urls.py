from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.search, name="search"),
    path('add/', views.add_movie, name="add_movie"),
    path('toggle/<int:movie_id>/', views.toggle_watched, name="toggle"),
    path('desc/<int:movie_id>/', views.update_description, name="desc"),
]