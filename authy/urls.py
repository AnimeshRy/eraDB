from django.urls import path
from .views import SignupView, EditProfile, UserProfile
from .views import like, unlike
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

app_name = "account"

urlpatterns = [
    path('login', LoginView.as_view(
        redirect_authenticated_user=True), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('profile/edit', EditProfile, name='edit-profile'),
    path('user/<username>', UserProfile, name='user-profile'),
    path('<username>/review/<imdb_id>/like', like, name='user-review-like'),
    path('<username>/review/<imdb_id>/unlike',
         unlike, name='user-review-unlike'),

]
