from django.urls import path
from .views import SignupView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

app_name = "account"

urlpatterns = [
    # sign up routes
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(
        redirect_authenticated_user=True), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]
