from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),

    path('create/', views.create_room, name="create_room"),
    path('join/', views.join_room, name="join_room"),

    path('room/<str:code>/', views.room_view, name="room"),

    path('room/<str:code>/search/', views.search, name="search"),
    path('room/<str:code>/add/', views.add_movie, name="add_movie"),

    path('room/<str:code>/toggle/<int:movie_id>/', views.toggle_watched, name="toggle"),
    path('room/<str:code>/desc/<int:movie_id>/', views.update_description, name="desc"),
]