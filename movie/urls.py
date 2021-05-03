from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('', views.index, name="index"),
    path('search/<query>/page/<page_number>',
         views.pagination, name="pagination"),
    path('<imdb_id>', views.movieDetails, name="movie-details")
]
