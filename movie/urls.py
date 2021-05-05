from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('', views.index, name="index"),
    path('search/<query>/page/<page_number>',
         views.pagination, name="pagination"),
    path('<imdb_id>', views.movieDetails, name="movie-details"),
    path('<imdb_id>/addmovietowatch',
         views.addMoviesToWatch, name="add-movie-to-watch"),
    path('<imdb_id>/addmovietowatched',
         views.addMoviesWatched, name="add-movie-to-watched"),
    path('genre/<slug:genre_slug>', views.genres, name="genres")
]
