from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as UserForm

class UserCreationForm(UserForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).\
            exclude(username=username).exists():

            raise forms.ValidationError(u'Email addresses must be unique.')

        return email


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', )

