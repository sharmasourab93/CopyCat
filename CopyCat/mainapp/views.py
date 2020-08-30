from django.shortcuts import render, Http404, redirect
from django.http import HttpResponseForbidden
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Imports related to Auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Imports related to Models, Forms, Parser
from .models import NewsFeed, Profile, UserDeleted
from .forms import LoginForm
from .parser import ParserClass


def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    
    if request.user.is_active and request.user.is_authenticated:
        
        return HttpResponseForbidden()
    
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
    another_form = UserCreationForm(request.POST or None)

    if request.user.is_active and request.user.is_authenticated:
        return HttpResponseForbidden()
    
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
    #TODO: Password Change/Password Forget
    pass


@login_required
def logout(request):
    logout(request)
    return render(request, "registration/logout.html")


# Delete Item Logical Function Written.
# TODO: URL for deleteitem remains.
@login_required
def deleteitem(request, hid):
    
    if request.user.is_active:
        user = User.objects.get(username=request.user)
        prof_user = Profile.objects.get(userid=user)
        hid = NewsFeed.objects.get(hid=hid)
        userdelete = None
        try:
            t = UserDeleted.objects.get(hid=hid)
        
        except ObjectDoesNotExist:
            userdelete = UserDeleted(userid=prof_user,
                                     hid=hid,
                                     delete=True)
            
        userdelete.save()
    
    return redirect(request, 'mainapp:index')
        

# Index Page populating logic
# written on 30-08-2020
@login_required
def index(request):
    items = ParserClass()
    items = items.get_fields()
    t = None
    
    for i in items:
        url, title = i[0], i[1]
        posted_on, author = i[2], i[3]
        hid, upvotes, comments = i[4], i[5], i[6]
        
        try:
            t = NewsFeed.objects.get(url=url)
            if t is not None:
                raise IntegrityError()
            
        except IntegrityError:
            t = NewsFeed.objects.get(url=url)
            t.comments = comments
            t.upvotes = upvotes
            t.posted_on = posted_on
            
        except ObjectDoesNotExist:
            t = NewsFeed(url=url, title=title,
                         hid=hid, posted_on=posted_on,
                         author=author, upvotes=upvotes,
                         comments=comments)
            
        finally:
            t.save()
        
    obj = NewsFeed.objects.all()
    context = {'data': obj}
    return render(request, 'mainapp/index.html', context)


@login_required
def profile(request, user):
    user_ = {'user': request.user}
    return render(request, "mainapp/profile.html", user_)


@login_required
def bookmark(request):
    bookmark = dict()
    user = {'user': User.username}
    return render(request, "mainapp/bookmarks.html", bookmark)


@login_required
def bookmark_details(request):
    pass
