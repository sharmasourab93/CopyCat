from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseForbidden
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Imports related to Auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Imports related to Models
from .models import NewsFeed, Profile
from .models import Bookmarks
from .models import UserDeleted, UserRead

# Forms & Parser import
from .forms import LoginForm, FillUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from .parser import ParserClass
import logging

# datetime features
from datetime import datetime


logger = logging.getLogger(__name__)


# 1. Sign Up - Register a User
def sign_up(request):
    # logger.info('SignUp for {0}'.format(request.user))
    context = {}
    form = UserCreationForm(request.POST or None)
    
    if request.user.is_active and request.user.is_authenticated:
        # logger.warning('Access Forbidden for {0}'.format(request.user))
        return HttpResponseForbidden()
    
    if request.method == "POST":
        # logger.debug('POST received. Redirecting to Filling')
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/filldetails/')
        
    context['form'] = form
    return render(request, 'registration/signup.html', context)


# 2. Fill Details Right after sign up.
@login_required
def filldetails(request):
    form = FillUpForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            profile_ = form.save()
            return redirect('/index/')
    
    context = {'form': form}
    return render(request, 'registration/details_page.html', context)


# 3. Login a user
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


# 4. Logout a user
@login_required
def logout(request):
    logout(request)
    return render(request, "registration/logout.html")


# 5. Password Change Not a priority
@login_required
def password_change(request):
    
    if request.method == 'POST' and request.user.is_active:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your Password was successfully updated!")
            return redirect('/accounts/login/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'registration/password.html', {'form': form})
    

# 6. Index Page populating logic
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


# 7. User's Profile View.
@login_required
def profile(request, user):
    context = {}
    if request.method == 'GET' and request.user.is_active:
        user_ = User.objects.get(username=user)
        prof_ = Profile.objects.get(user=user_)
        
        context['data'] = prof_
        
    return render(request, "mainapp/profile.html", context)


# 8. Read History View.
@login_required
def marked_read(request):
    read_history = dict()
    user = User.objects.get(username=request.user)
    prof = Profile.objects.get(user=user)
    marks = UserRead.objects.filter(userid=prof) \
        .values_list('hid_id')
    
    obj = NewsFeed.objects.filter(id__in=marks).order_by('posted_on')
    
    read_history['data'] = obj
    
    return render(request, "mainapp/history.html", read_history)


# 9. Mark a URL as Read
@login_required
def marked_read_detail(request, hid):
    user = User.objects.get(username=request.user)
    prof = Profile.objects.get(user=user)
    nfd = NewsFeed.objects.get(hid=hid)
    
    if request.user.is_active and \
            request.method == 'POST' and \
            hid is not None:
        
        try:
            user_read = UserRead.objects.get(hid=nfd, userid=prof)
        
        except ObjectDoesNotExist:
            user_read = UserRead(userid=prof, hid=nfd)
            user_read.save()
    
    return HttpResponse(status=204)


# 10. Bookmark a URL
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


# 11. Bookmark Details.
@login_required
def bookmark_details(request, hid):
    user = User.objects.get(username=request.user)
    nfd = NewsFeed.objects.get(hid=hid)
    prof = Profile.objects.get(user=user)

    if request.user.is_active and request.method == 'POST':
        if 'remove' not in request.META['PATH_INFO']:
            try:
                user_read = Bookmarks.objects.get(hack_id=nfd, user=prof)
                
            except ObjectDoesNotExist:
                user_read = Bookmarks(user=prof, hack_id=nfd)
                user_read.save()
                
            return HttpResponse(status=204)
    
        else:
            try:
                user_read = Bookmarks.objects.get(hack_id=nfd, user=prof)
                user_read.delete()
            
            except ObjectDoesNotExist:
                pass

            return redirect('/bookmark/')
            

# 12. Delete Item Logical Function Written.
@login_required
def deleteitem(request, hid):
    if request.user.is_active and request.method == 'POST':
        user = User.objects.get(username=request.user)
        prof_user = Profile.objects.get(user=user)
        hid_ = NewsFeed.objects.get(hid=hid)
        
        try:
            userdel = UserDeleted.objects.get(hid=hid,
                                              userid=prof_user)
            return HttpResponse(status=204)
        
        except ObjectDoesNotExist:
            userdel = UserDeleted(userid=prof_user,
                                  hid=hid_,
                                  deleted=True)
        
        userdel.save()
    
    return redirect('/index/')
