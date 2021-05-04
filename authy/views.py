from django.shortcuts import render
from django.views.generic import CreateView
from .forms import SignUpForm
from django.urls import reverse


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("account:login")
