from django.contrib.auth.models import User
import requests


def get_youtube_video(film):
    result = "+".join(film.split()) + '+'
    json = requests.get('https://www.youtube.com/results?search_query=' + result.lower() + "+trailer%20espanol")
    point = json.text.find('/watch?v=')
    return 'https://www.youtube.com/embed/' + json.text[point + 9:point + 20]


class objectFilm:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.year = ""
        self.url_image = ""
        self.score = ""
        self.director = ""
        self.crew = ""
        self.video = ""
