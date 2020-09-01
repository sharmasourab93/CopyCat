from django.shortcuts import render, Http404, redirect
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# django Urls related
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

# Imports related to Auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Imports related to Models, Forms, Parser
from .models import NewsFeed, Profile
from .models import Bookmarks
from .models import UserDeleted, UserRead
from .forms import LoginForm
from .parser import ParserClass

# datetime features
from datetime import datetime

def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    
    if request.user.is_active and request.user.is_authenticated:
        
        return HttpResponseForbidden()
    
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            return redirect(request, 'mainapp:login')
        
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
    
    if request.user.is_active and request.method == 'POST':
        user = User.objects.get(username=request.user)
        prof_user = Profile.objects.get(user=user)
        hid_ = NewsFeed.objects.get(hid=hid)
        
        try:
            userdel = UserDeleted.objects.get(hid=hid,
                                              userid=prof_user)
        
        except ObjectDoesNotExist:
            userdel = UserDeleted(userid=prof_user,
                                  hid=hid_,
                                  deleted=True)
            
        userdel.save()
    
    return redirect('/index/')
        

# Index Page populating logic
# written on 30-08-2020
@login_required
def index(request):
    items = ParserClass()
    items = items.get_fields()
    t = None
    
    for i in items:
        url, title = i[0], i[1]
        author = i[3]
        posted_on = datetime.strptime(i[4], "%d-%m-%Y %H:%M:%S")
        hid, upvotes, comments = i[2], i[5], i[6]
        
        try:
            t = NewsFeed.objects.get(url=url)
            if t is not None:
                raise IntegrityError()
            
        except IntegrityError:
            t = NewsFeed.objects.get(url=url)
            t.comments = comments
            t.upvotes = upvotes
            
        except ObjectDoesNotExist:
            t = NewsFeed(url=url, title=title,
                         hid=hid, posted_on=posted_on,
                         author=author, upvotes=upvotes,
                         comments=comments)
            
        finally:
            t.save()
    
    # Exclude items that exists in Userdeleted table
    # 1. Query for the authenticated user.
    # 2. Profile On the Aunthenticated User.
    # 3. Query the Deleted Data for the User
    user = User.objects.get(username=request.user)
    prof = Profile.objects.get(user=user)
    userdel = UserDeleted.objects.filter(userid=prof)\
        .values_list('hid_id', flat=True)
    
    # 4. Exclude the deleted Item for the user.
    obj = NewsFeed.objects.order_by("posted_on").reverse()
    obj = obj.exclude(id__in=userdel)
    
    
    context = {'data': obj}
    return render(request, 'mainapp/index.html', context)


@login_required
def profile(request, user):
    user_ = {'user': request.user}
    return render(request, "mainapp/profile.html", user_)


@login_required
def bookmark(request):
    bookmark = dict()
    user = User.objects.get(username=request.user)
    prof = Profile.objects.get(user=user)
    marks = Bookmarks.objects.filter(user=prof)\
        .values_list('hack_id_id')
    
    obj = NewsFeed.objects.filter(id__in=marks).order_by("posted_on")
    
    bookmark['data'] = obj
    
    return render(request, "mainapp/bookmarks.html", bookmark)


@login_required
def bookmark_details(request, hid):
    user = User.objects.get(username=request.user)
    nfd = NewsFeed.objects.get(hid=hid)
    prof = Profile.objects.get(user=user)
    print("Printing HID", hid)
    if request.user.is_active and request.method == 'POST':
        try:
            user_read = Bookmarks.objects.get(hack_id=nfd, user=prof)
            #TODO: Find a way to figure out bookmarking without
            # redirecting/re-loading the web page
            return redirect(reverse('/index/'))
        
        except NoReverseMatch:
            return redirect('/index/')
            
        except ObjectDoesNotExist:
            user_read = Bookmarks(user=prof, hack_id=nfd)
            user_read.save()
            return HttpResponseRedirect('/index/')
    
    elif request.user.is_active and request.method == 'GET':
        print(request.method)
        try:
            user_read = Bookmarks.objects.get(hack_id=nfd, user=prof)
            user_read.delete()
            return redirect('/bookmark/')
        
        except ObjectDoesNotExist:
            return redirect('/bookmark/')
