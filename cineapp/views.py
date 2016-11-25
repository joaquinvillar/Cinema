from django.shortcuts import render
import datetime
# Create your views here.
from django.views import generic
from .models import Cine, Sala, MovieSala, Movie


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
        data["movie"] = pk
        salas = {}
        rooms = MovieSala.objects.filter(movie=self)
        for roo in rooms:
            roomlist = MovieSala.objects.filter(movie=self, sala=roo.sala_id)
            sum = datetime.timedelta()
            for room in roomlist:
                sum += room.end-room.begin
                print room.end-room.begin
            salas[roo.sala_id] = str(sum)
        data["salas"] = salas
        return render(request, self.template_name, data)


        # hola = 123
        # render(request, self.template_name, {"salas": {"sala1": 123, "sala2": 123}, "movies":[movie1, movie2]})





