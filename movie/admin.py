from django.contrib import admin
from .models import Movie, Rating, Genre, Review

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Genre)
