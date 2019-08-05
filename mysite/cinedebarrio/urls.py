from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_film', views.add_film, name='add_film'),
    path('login', views.login, name='login'),
    path('login_process', views.login_process, name='login_process'),
    path('logout', views.logout, name='logout'),
    path('admin', views.admin, name='admin'),
    path('admin_users', views.admin_users, name='admin_users'),
    path('admin_films', views.admin_films, name='admin_films'),
    path('add_users', views.add_users, name='add_users'),
    path('edit_users', views.edit_users, name='edit_users'),
    path('edit', views.edit, name='edit'),
    path('edit_films', views.edit_films, name='edit_films'),
    path('edit_2', views.edit_2, name='edit_2'),
    path('delete_users', views.delete_users, name='delete_users'),
    path('add', views.add, name='add'),
    path('search_film', views.search_film, name='search_film'),
    path('add_film_manual', views.add_film_manual, name='add_film_manual'),
    path('delete_film', views.delete_film, name='delete_film'),
    path('search_film_user', views.search_film_user, name='search_film_user'),
    path('film', views.film, name='film')
]
