from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'mainapp/index.html')
        
    context['form'] = form
    return render(request, 'registration/signup.html', context)


def login_user(request):
    context = dict()
    form = LoginForm()
    
    if request.method == 'GET':
        context = {'form': form}
        return render(request, 'registration/login.html', context)
    
    else:
        user = form.login(request)
        
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'mainapp/index.html', {'user': user})
            
        invalid = {'message': "Invalid Login", 'form': form}
        return render(request, "registration/login.html", invalid)
        

@login_required
def password_change(request):
    pass


@login_required
def logout(request):
    logout(request)
    return render(request, "registration/logout.html")


@login_required
def index(request):
    user = {'user': request.user}
    return render(request, 'mainapp/index.html', user)


@login_required
def profile(request, user):
    user_ = {'user': request.user}
    return render(request, "mainapp/profile.html", user_)


@login_required
def bookmark(request):
    bookmark = {'abc': 'abc'}
    user = {'user': User.username}
    
    return render(request, "mainapp/bookmarks.html", bookmark, user)


@login_required
def bookmark_details(request):
    pass
