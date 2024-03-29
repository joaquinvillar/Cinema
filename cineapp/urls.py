#  url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
# url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
# url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),


from django.conf.urls import url

from . import views

app_name = 'cineapp'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^movie/(?P<pk>[0-9]+)/$', views.DetailViewMovie.as_view(), name='detailmovie'),
    url(r'^cinema/(?P<pk>[0-9]+)/$', views.DetailViewCinema.as_view(), name='detailcinema'),
    url(r'^sign/', views.sig_in, name='sign'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^upload/$', views.model_form_upload, name='upload'),
]
