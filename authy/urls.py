from django.urls import path
from .views import SignupView, EditProfile, UserProfile
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

app_name = "account"

urlpatterns = [
    path('profile/edit', EditProfile, name='edit-profile'),
    path('<username>', UserProfile, name='user-profile'),
    # sign up routes
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(
        redirect_authenticated_user=True), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]
