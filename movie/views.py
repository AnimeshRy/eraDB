from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.utils.text import slugify
from .models import Movie, Genre, Rating, Review
from actor.models import Actor
from django.core.paginator import Paginator
from authy.models import Profile
from django.urls import reverse
from .forms import RateForm
from django.db.models import Avg
import os
import dotenv
import requests

dotenv.load_dotenv()
APIKEY = str(os.getenv('omdbKey'))


def index(request):
    query = request.GET.get('q')
    if query:
        url = f'http://omdbapi.com/?apikey={APIKEY}&s={query}'
        response = requests.get(url)
        movie_data = response.json()

        context = {
            'query': query,
            'movie_data': movie_data,
            'page_number': 2
        }
        template = loader.get_template('search_results.html')
        return HttpResponse(template.render(context, request))
    return render(request, "index.html")


def pagination(request, query, page_number):
    # load more pages from API
    url = f'http://omdbapi.com/?apikey={APIKEY}&s={query}&page={str(page_number)}'
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1

    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number
    }
    template = loader.get_template('search_results.html')
    return HttpResponse(template.render(context, request))


def movieDetails(request, imdb_id):
    if Movie.objects.filter(imdbID=imdb_id).exists():
        movie_data = Movie.objects.get(imdbID=imdb_id)
        reviews = Review.objects.filter(movie=movie_data)
        reviews_avg = reviews.aggregate(Avg('rate'))
        reviews_count = reviews.count()
        our_db = True

        context = {
            'movie_data': movie_data,
            'reviews': reviews,
            'reviews_avg': reviews_avg,
            'reviews_count': reviews_count,
            'our_db': our_db,
        }
    else:
        url = f'http://omdbapi.com/?apikey={APIKEY}&i={imdb_id}'
        response = requests.get(url)
        movie_data = response.json()

        # Inject to our database

        rating_objs = []
        genre_objs = []
        actor_objs = []

        # Actors Logic
        actor_list = [x.strip() for x in movie_data['Actors'].split(',')]

        for actor in actor_list:
            a, created = Actor.objects.get_or_create(name=actor)
            actor_objs.append(a)

        # Genre Logic
        genre_list = list(movie_data['Genre'].replace(" ", "").split(','))

        for genre in genre_list:
            genre_slug = slugify(genre)
            g, created = Genre.objects.get_or_create(
                title=genre, slug=genre_slug)
            genre_objs.append(g)

        # Rating Logic
        for rate in movie_data['Ratings']:
            r, created = Rating.objects.get_or_create(
                source=rate['Source'], rating=rate['Value'])
            rating_objs.append(r)

        if movie_data['Type'] == 'movie':
            if movie_data['Poster'] == "N/A":
                PosterURL = ""
            else:
                PosterURL = movie_data['Poster']
            # save movie info
            m, created = Movie.objects.get_or_create(
                Title=movie_data['Title'],
                Year=movie_data['Year'],
                Rated=movie_data['Rated'],
                Released=movie_data['Released'],
                Runtime=movie_data['Runtime'],
                Director=movie_data['Director'],
                Writer=movie_data['Writer'],
                Plot=movie_data['Plot'],
                Language=movie_data['Language'],
                Country=movie_data['Country'],
                Awards=movie_data['Awards'],
                Poster_url=PosterURL,
                Metascore=movie_data['Metascore'],
                imdbRating=movie_data['imdbRating'],
                imdbVotes=movie_data['imdbVotes'],
                imdbID=movie_data['imdbID'],
                Type=movie_data['Type'],
                DVD=movie_data['DVD'],
                BoxOffice=movie_data['BoxOffice'],
                Production=movie_data['Production'],
                Website=movie_data['Website'],)

            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(rating_objs)

        else:
            # save series info
            if movie_data['Poster'] == "N/A":
                PosterURL = ""
            else:
                PosterURL = movie_data['Poster']
            m, created = Movie.objects.get_or_create(
                Title=movie_data['Title'],
                Year=movie_data['Year'],
                Rated=movie_data['Rated'],
                Released=movie_data['Released'],
                Runtime=movie_data['Runtime'],
                Director=movie_data['Director'],
                Writer=movie_data['Writer'],
                Plot=movie_data['Plot'],
                Language=movie_data['Language'],
                Country=movie_data['Country'],
                Awards=movie_data['Awards'],
                Poster_url=PosterURL,
                Metascore=movie_data['Metascore'],
                imdbRating=movie_data['imdbRating'],
                imdbVotes=movie_data['imdbVotes'],
                imdbID=movie_data['imdbID'],
                Type=movie_data['Type'],
                totalSeasons=movie_data['totalSeasons'],
            )

            m.Genre.set(genre_objs)
            m.Actors.set(actor_objs)
            m.Ratings.set(rating_objs)

        # save movie info for actors
        for actor in actor_objs:
            actor.movies.add(m)
            actor.save()

        m.save()
        our_db = False

        context = {
            'movie_data': movie_data,
            'our_db': our_db
        }

    template = loader.get_template('movie_details.html')
    return HttpResponse(template.render(context, request))


def genres(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    movies = Movie.objects.filter(Genre=genre)

    # pagination
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'genre': genre
    }
    template = loader.get_template('genre.html')
    return HttpResponse(template.render(context, request))


def addMoviesToWatch(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user
    profile = Profile.objects.get(user=user)
    profile.to_watch.add(movie)

    return HttpResponseRedirect(reverse('movie:movie-details', args=[imdb_id]))


def addMoviesWatched(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if profile.to_watch.filter(imdbID=imdb_id).exists():
        profile.to_watch.remove(movie)
        profile.watched.add(movie)
    else:
        profile.watched.add(movie)

    return HttpResponseRedirect(reverse('movie:movie-details', args=[imdb_id]))


def Rate(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = user
            rate.movie = movie
            rate.save()
            return HttpResponseRedirect(reverse('movie:movie-details', args=[imdb_id]))
    else:
        form = RateForm()

    template = loader.get_template('rate.html')

    context = {
        'form': form,
        'movie_data': movie,
    }

    return HttpResponse(template.render(context, request))
