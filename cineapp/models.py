from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
import datetime
import json

# Create your models here.


class Cine(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=200)
    birth = models.DateTimeField('date published')

    def __unicode__(self):
        return self.name


class MovieSala(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    sala = models.ForeignKey("Sala", on_delete=models.CASCADE)
    begin = models.DateTimeField('Begining')
    end = models.DateTimeField('End')

    def __unicode__(self):
        return "%s - %s" % (self.movie, self.sala)


class MovieActors(models.Model):
    principal = models.BooleanField(default=False)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    actor = models.ForeignKey("Actor", on_delete=models.CASCADE)

    def __unicode__(self):
        return "%s - %s" % (self.movie, self.actor)


class Movie(models.Model):
    name = models.CharField(max_length=200)
    actors = models.ManyToManyField(Actor, through=MovieActors)

    def __unicode__(self):
        return self.name

    def next_room(self):
        now = timezone.now()
        return self.sala_set.filter(moviesala__begin__gt=now)

    def reprod(self):
        now = timezone.now()
        return self.sala_set.filter(moviesala__end__lt=now).count()

    def get_duration(self):
        data = {}
        rooms = MovieSala.objects.filter(movie=self)
        for roo in rooms:
            roomlist = MovieSala.objects.filter(movie=self, sala=roo.sala_id)
            sum = datetime.timedelta()
            for room in roomlist:
                sum += room.end-room.begin
                print room.end-room.begin
            data[roo.sala_id] = str(sum)
        json_data = json.dumps(data)
        return json_data


class Sala(models.Model):
    number = models.IntegerField(default=0)
    encargado = models.CharField(max_length=200)
    cine = models.ForeignKey(Cine, on_delete=models.CASCADE)
    movie = models.ManyToManyField(Movie, through=MovieSala)

    def __unicode__(self):
        return "%s" % self.number

    def is_playing_movie(self):
        now = timezone.now()
        reprod = self.moviesala_set.filter(end__gt=now, begin__lt=now)
        if reprod:
            return True
        else:
            return False

    def play_movies(self):
        today = timezone.now()
        movies = self.moviesala_set.filter(end__lt=today)
        return movies





