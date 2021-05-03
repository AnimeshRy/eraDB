from django.shortcuts import render
import os
import dotenv
import requests
dotenv.load_dotenv()


def index(request):
    APIKEY = str(os.getenv('omdbKey'))
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
        return render(request, "search_results.html", context=context)
    return render(request, "index.html")


def pagination(request, query, page_number):
    APIKEY = str(os.getenv('omdbKey'))
    url = f'http://omdbapi.com/?apikey={APIKEY}&s={query}&page={str(page_number)}'
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1

    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number
    }
    return render(request, "search_results.html", context=context)
