from django.urls import path
from .views import SignupView, EditProfile, UserProfile
from .views import like, unlike, UserProfileMoviesWatched, UserProfileSeriesWatched, UserProfileWatchList, UserProfileMoviesReviewed
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
    path('<username>/movieswatched', UserProfileMoviesWatched,
         name='profile-movies-watched'),
    path('<username>/serieswatched', UserProfileSeriesWatched,
         name='profile-series-watched'),
    path('<username>/watchlist', UserProfileWatchList, name='profile-watch-list'),
    path('<username>/reviewed', UserProfileMoviesReviewed,
         name='profile-reviewed-list'),
    path('<username>/review/<imdb_id>/like', like, name='user-review-like'),
    path('<username>/review/<imdb_id>/unlike',
         unlike, name='user-review-unlike'),


]
