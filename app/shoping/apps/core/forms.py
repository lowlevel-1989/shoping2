from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as UserForm

class UserCreationForm(UserForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', )

