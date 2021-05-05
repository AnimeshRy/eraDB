from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class EditProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    first_name = forms.CharField(
        widget=forms.TextInput(), max_length=50, required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(), max_length=50, required=False)
    location = forms.CharField(
        widget=forms.TextInput(), max_length=25, required=False)
    url = forms.CharField(widget=forms.TextInput(), label='Website',
                          max_length=100, required=False)
    profile_info = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 3}), label='About You', max_length=150, required=False)

    class Meta:
        model = Profile
        fields = ('picture', 'first_name', 'last_name',
                  'location', 'url', 'profile_info')
