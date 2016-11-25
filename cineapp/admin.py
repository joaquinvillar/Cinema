from django.contrib import admin
from .models import Sala, Movie, Cine, Actor, MovieSala, MovieActors
# Register your models here.

admin.site.register(Sala)
admin.site.register(Movie)
admin.site.register(Cine)
admin.site.register(Actor)
admin.site.register(MovieSala)
admin.site.register(MovieActors)

