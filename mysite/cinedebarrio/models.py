from django.db import models


class Film(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.CharField(max_length=300)
    description = models.CharField(max_length=200)
    year = models.IntegerField()
    director = models.CharField(max_length=50)
    actors = models.CharField(max_length=200)
    poster = models.CharField(max_length=300)
    score = models.FloatField()
