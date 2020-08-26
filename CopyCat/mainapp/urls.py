from django.contrib import admin
from django.urls import path
from .views import index, sign_up, logout, login_user, password_change
from .views import profile, bookmark

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
    path(r'profile/<user>', profile, name='profile'),
    
    # Bookmarks or List View
    path('bookmark/', bookmark, name='bookmark'),
    # Detail View/ View at every news Item
    # path('bookmark/^(?P<url_id>\w+)$', bookmark_detail, name="details"),
    ]
