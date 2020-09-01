from django.contrib import admin
from django.urls import path, re_path
from .views import index, sign_up, logout, login_user, password_change
from .views import profile, bookmark
from .views import deleteitem, bookmark_details

app_name = 'mainapp'

urlpatterns = [
    
    # 1. Creating Users/Sign Up
    path('accounts/signup', sign_up, name="sign-up"),
    # 2. Login
    path('accounts/login', login_user, name="login"),
    # 3. Logout
    path('accounts/logout', logout, name="logout"),
    # 4. Password Change
    #TODO: Password Change/Reset
    
    # 5. Index View With News View
    path('index/', index, name='index'),
    
    # 6. User's Profile View
    #TODO: Profile View In Template & views.py
    path(r'profile/<user>', profile, name='profile'),
    
    # 7. Marked As Read
    #TODO: URLS Marked As Read
    # re_path(r'^index/read/(?P<hid>[0-9]+)/$', marked_read, name="marked_read")
    
    # 8. Bookmarks or View All Bookmarks
    path('bookmark/', bookmark, name='bookmark'),
    # 9. Add Bookmark
    re_path(r'^index/bookmark/(?P<hid>[0-9]+)/$', bookmark_details, name="details"),
    # 10. Remove Bookmarks
    re_path(r'^bookmark/remove/(?P<hid>[0-9]+)$', bookmark_details, name="details"),
    
    # 11. Delete Item from a user's view.
    re_path(r'^index/deleteitem/(?P<hid>[0-9]+)/$', deleteitem, name="deleteitem")
    ]
