from django.urls import path
from actor import views

app_name = "actor"

urlpatterns = [
    path('<slug:actor_slug>', views.actors, name='actors'),
]
