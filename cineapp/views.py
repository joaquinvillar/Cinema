from django.shortcuts import render
import datetime
# Create your views here.
from django.views.generic import View
from django.utils import timezone
from django.views import generic
from .models import Cine, Sala, MovieSala, Movie, MovieActors
from django.contrib.auth import authenticate, login, logout, settings
from django.http import HttpResponse, HttpResponseRedirect


class IndexView(generic.ListView):
    template_name = 'cineapp/index.html'
    context_object_name = 'cine_list'

    def get_queryset(self):
        return Cine.objects.all()


class DetailView(generic.DetailView):
    model = Sala
    template_name = 'cineapp/detail.html'


class DetailViewMovie(generic.View):
    model = Movie
    template_name = 'cineapp/detailmovie.html'
    context_object_name = 'list_room'

    def get(self, request, pk):
        data = {}
        mov = Movie.objects.get(id=pk).name
        data["rep"] = Movie.objects.get(id=pk).reprod()
        data["movie"] = mov
        actors = {}
        act = MovieActors.objects.filter(movie__id=pk)
        for actor in act:
            actors[actor.actor.id] = actor.actor.name
        data["actors"] = actors
        salas = {}
        sig = {}
        now = timezone.now()
        # looks for the next rep of the movie on each room
        rooms = MovieSala.objects.filter(movie=pk)
        for roo in rooms:
            roomlist = MovieSala.objects.filter(movie=pk, sala=roo.sala_id)
            sum = datetime.timedelta()
            for room in roomlist:
                sum += room.end-room.begin
            salas[roo.sala_id] = str(sum)
        data["salas"] = salas

        now = timezone.now()
        rooms = MovieSala.objects.filter(movie=pk, begin__gt=now)
        for roo in rooms:
            roomlist = MovieSala.objects.filter(movie=pk, sala=roo.sala_id, begin__gt=now)
            sig[roo.sala_id] = str(roomlist.get().begin)
        data["sig"] = sig
        return render(request, self.template_name, {"data": data})


        # hola = 123
        # render(request, self.template_name, {"salas": {"sala1": 123, "sala2": 123}, "movies":[movie1, movie2]})


class DetailViewCinema(generic.View):
    template_name = 'cineapp/detailcinema.html'

    def get(self, request, pk):
        ret = {}
        ret["movie"] = Cine.objects.get(id=pk).name
        dmovies = {}
        rooms = Sala.objects.filter(cine__pk=pk)
        ret["nrooms"] = rooms.count()
        for room in rooms:
            movies = room.movie.all()
            for movie in movies:
                dmovies[movie.id] = movie
        ret["movies"] = dmovies
        return render(request, self.template_name, {"ret": ret})


class Sign(generic.View):
    template_name = 'cineapp/sign.html'

    def get(self, request):
        ret = {}
        return render(request, self.template_name, {"retu": ret})


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/form')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

        return render(request, "index.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)



