import requests
from cinedebarrio.models import Film
from cinedebarrio.utils import get_youtube_video, objectFilm
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.models import User

url_api_movie = "https://api.themoviedb.org/3/search/movie?"
url_api_actors = "https://api.themoviedb.org/3/movie/"
api_token = "dae3f3329b99aa6d8a53945041678772"
server_images = "https://image.tmdb.org/t/p/w500/"


def index(request):
    template = loader.get_template("cinedebarrio/index.html")
    list_films = []

    # GetFilms DB
    for e in Film.objects.order_by('?'):
        list_films.append(e)

    context = {
        'list_films': list_films
    }

    return HttpResponse(template.render(
        context, request))


def film(request):
    if request.user.is_authenticated:
        template = loader.get_template("cinedebarrio/film.html")
        filtered_film = Film.objects.filter(name=request.POST['film_search'])
        stars = []

        for a in range(0, round(filtered_film[0].score)):
            stars.append(a)

        context = {
            'film': filtered_film[0],
            'stars': stars
        }

        return HttpResponse(template.render(
            context, request))
    else:
        return redirect('login')


def search_film_user(request):
    template = loader.get_template("cinedebarrio/search_film_user.html")

    list_films = []

    if request.POST['input_search'] != '':
        filtered_films = Film.objects.filter(name__contains=request.POST['input_search'])
        for e in filtered_films:
            list_films.append(e)

    context = {
        "list_films": list_films
    }

    return HttpResponse(template.render(
        context, request))


def add_film_manual(request):
    film = Film()
    film.name = request.POST['name']
    film.url = request.POST['url']
    film.description = request.POST['description']
    film.year = request.POST['year']
    film.director = request.POST['director']
    film.actors = request.POST['actors']
    film.poster = request.POST['poster']

    film.score = request.POST['score']
    film.save()

    list_films = []

    filtered_films = Film.objects.filter(name__contains=request.POST['name'])
    for e in filtered_films:
        list_films.append(e)

    template = loader.get_template("cinedebarrio/search_film_user.html")

    context = {
        "list_films": list_films
    }

    return HttpResponse(template.render(
        context, request))


def add_film(request):
    global url_api_movie, url_api_actors, api_token, server_images

    template = loader.get_template("cinedebarrio/search_film_user.html")
    listFilms = []

    try:
        # if is null
        if request.POST['film_search'] != '':

            # Search film API
            peliculaBuscada = request.POST['film_search']
            headers = {"api_key": api_token,
                       "language": "es-ES",
                       "query": peliculaBuscada,
                       "page": "1",
                       "include_adult": "false"}
            r = requests.get(url_api_movie, headers)
            json_pelicula = r.json()

            # LLamada para obtener el reparto
            headers = {"api_key": api_token}

            for i in range(0, len(json_pelicula['results'])):

                if json_pelicula['results'][i]['overview'] != '':
                    film = objectFilm()
                    film.title = json_pelicula['results'][i]['title']
                    film.description = json_pelicula['results'][i]['overview']
                    film.year = json_pelicula['results'][i]['release_date']
                    film.year = film.year[0:4]
                    film.url_image = server_images + json_pelicula['results'][i]['poster_path'][1:]
                    film.score = json_pelicula['results'][i]['vote_average']

                    r = requests.get(url_api_actors + str(json_pelicula['results'][i]['id']) + "/credits?", headers)
                    json_crew = r.json()

                    director = ""
                    crew = ""

                    for j in range(0, len(json_crew['crew'])):
                        if json_crew['crew'][j]['job'] == 'Director':
                            director = json_crew['crew'][j]['name']

                    for j in range(0, len(json_crew['cast'])):
                        crew += json_crew['cast'][j]['name'] + ", "

                    film.director = director
                    film.crew = crew

                    # Llamada a youtube
                    video = get_youtube_video(json_pelicula['results'][i]['title'])
                    film.video = video + "?rel=0&amp;showinfo=0"

                    listFilms.append(film)

                    p = Film(name=film.title,
                             description=film.description,
                             url=film.video,
                             year=int(film.year),
                             director=film.director,
                             actors=film.crew,
                             poster=film.url_image,
                             score=float(film.score))
                    p.save()

            context = {
                "films": listFilms
            }

    except:
        print('Error de servicio')

    finally:

        list_films = []

        filtered_films = Film.objects.filter(name__contains=request.POST['film_search'])
        for e in filtered_films:
            list_films.append(e)

        context = {
            "list_films": list_films
        }

        return HttpResponse(template.render(
            context, request))


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        template = loader.get_template("cinedebarrio/login.html")
        context = {}
        return HttpResponse(template.render(context, request))


def login_process(request):
    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        return redirect('index')
    else:
        template = loader.get_template("cinedebarrio/login.html")
        context = {'error': 'Username and password doesnt match Please try again '}
        return HttpResponse(template.render(context, request))


def logout(request):
    auth.logout(request)
    return redirect('index')


def admin(request):
    template = loader.get_template("cinedebarrio/admin.html")
    context = {}
    return HttpResponse(template.render(
        context, request))


def admin_users(request):
    template = loader.get_template("cinedebarrio/admin_users.html")
    users = User.objects.all()
    context = {'users': users}
    return HttpResponse(template.render(
        context, request))


def add(request):
    template = loader.get_template("cinedebarrio/add_user.html")
    context = {}
    return HttpResponse(template.render(
        context, request))


def add_users(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username, email, password)
    user.save()
    return redirect('admin')


def edit(request):
    user = request.POST['user']
    template = loader.get_template("cinedebarrio/edit_users.html")
    context = {'username': user}
    return HttpResponse(template.render(
        context, request))


def edit_users(request):
    u = User.objects.get(username=request.POST['oldUsername'])
    u.username = request.POST['username']
    u.password = request.POST['password']
    u.email = request.POST['email']
    u.save()
    return redirect('admin_users')


def delete_users(request):
    u = User.objects.get(username=request.POST['user'])
    u.delete()
    return redirect('admin_users')


def search_film(request):
    template = loader.get_template("cinedebarrio/search_film.html")
    context = {}
    return HttpResponse(template.render(
        context, request))


def admin_films(request):
    template = loader.get_template("cinedebarrio/admin_films.html")
    films = Film.objects.order_by('name')
    films_ar = []
    for e in films:
        films_ar.append(e)
    context = {'films': films_ar}
    return HttpResponse(template.render(
        context, request))


def edit_films(request):
    film_name = request.POST['film']
    print(film_name)
    film = Film.objects.get(name=film_name)
    template = loader.get_template("cinedebarrio/edit_films.html")
    context = {'film': film}
    return HttpResponse(template.render(
        context, request))


def edit_2(request):
    film = Film.objects.get(name=request.POST['name'])
    film.name = request.POST['name_edit']
    film.url = request.POST['url']
    film.description = request.POST['description']
    film.year = int(request.POST['year'])
    film.director = request.POST['director']
    film.actors = request.POST['actors']
    film.poster = request.POST['poster']
    film.score = float(request.POST['score'])
    film.save()
    return redirect('admin_films')


def delete_film(request):
    name = request.POST['film']
    film = Film.objects.get(name=name)
    film.delete()
    return redirect('admin_films')
