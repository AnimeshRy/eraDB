from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('', views.index, name="search"),
    path('search/<query>/page/<page_number>',
         views.pagination, name="pagination")
]
