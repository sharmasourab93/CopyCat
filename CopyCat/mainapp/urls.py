from django.contrib import admin
from django.urls import path, re_path
from .views import index, sign_up, logout, login_user, password_change
from .views import profile, bookmark
from .views import deleteitem, bookmark_details

app_name = 'mainapp'

urlpatterns = [
    
    # Creating Users/Sign Up
    path('accounts/signup', sign_up, name="sign-up"),
    # Login
    path('accounts/login', login_user, name="login"),
    # Logout
    path('accounts/logout', logout, name="logout"),
    # Password Change
    # pass
    
    # Index View With News View
    path('index/', index, name='index'),
    
    #User's Profile View
    #TODO: Profile View
    path(r'profile/<user>', profile, name='profile'),
    
    #TODO:
    
    # Bookmarks or List View
    path('bookmark/', bookmark, name='bookmark'),
    # Detail View/ View at every news Item
    re_path(r'^index/bookmark/(?P<hid>[0-9]+)/$', bookmark_details, name="details"),
    re_path(r'^bookmark/unbookmark/(?P<hid>[0-9]+)$', bookmark_details, name="details"),
    
    # Delete View
    re_path(r'^index/deleteitem/(?P<hid>[0-9]+)/$', deleteitem, name="deleteitem")
    ]
