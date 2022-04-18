from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class UserForm(UserCreationForm):

    first_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    type = forms.CharField(max_length=30)
    category = forms.CharField(max_length=30)
    profile_path = forms.CharField(max_length=200)
    # last_name = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ("username", "password1", "password2","first_name","phone", "type", "category", "profile_path")

# class UserForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30)
#     # last_name = forms.CharField(max_length=150)
#     class Meta:
#         model = User
#         fields = ("username", "first_name")
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')