from .models import Tweet
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TweetForm(forms.ModelForm):
    class Meta:
        model=Tweet
        fields=['text','photo']

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class meta:
        model=User
        fields=('username','email','password1','password2')