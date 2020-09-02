from django.contrib.auth.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)

    def login(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        return user
    

class PasswordChange(forms.Form):
    pass


class FillUpForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['user', 'name',
                  'email', 'bday']
