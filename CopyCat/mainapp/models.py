from django.db import models
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta


# Create your models here.
class NewsFeed(models.Model):
    """
    News Feed Model has the following columns:
        id  Integer Primary KEY
        url CharField Unique
        title Charfield
        hid Charfield HackerNewsID
        author Charfield
        postedon Charfield Time in String
        upvotes Integer Count of Integers
        comments Integer Count of Integers
        
        The above mentioned fields will be inserted
        on every new item found in the hackernews site.
        
        The following are the fields that will be updated
        on finding the existing item:
        1. posted_on
        2. upvotes
        3. Comments
        
    """
    id = models.AutoField(primary_key=True)
    
    # URL & Title can be extracted together
    url = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    
    # On Hackernews site, Clicking on time stamp tables redirects to H-ID.
    # For sample: https://news.ycombinator.com/item?id=24271898
    hid = models.CharField(max_length=255, unique=True)
    
    # author name
    author = models.CharField(max_length=50)
    
    # posted_on was initially taken as a character
    # and displayed as such. Requirement is to display in
    # reverse chronological order.
    # One way to do can be to preserver the character field input,
    # but priority is to have the field in DateTimeField type
    
    # Parser model returns input in the time format,
    # hence the below two lines are commented out.
    
    # posted_on = models.CharField(max_length=50)
    # datefield = models.DateField(blank=True, null=True)
    
    # News field model altered on 31-08-2020.
    posted_on = models.DateTimeField(editable=False, default=datetime.now)
    
    # Upvotes posted in Points
    upvotes = models.IntegerField()
    
    # Comments redirect to H-ID'd page.
    comments = models.IntegerField()
    
    """
    # The below given method overrides saving of the field to prefill
    # for fields where entry hasn't be consumed in the arguments.
    # The below method is commented out as the parser module
    # returns in DateTimeField format from the provided CharField.
    def save(self, *args, **kwargs):
        if self.datefield is None:
            if 'minutes' in self.posted_on:
                self.datefield = datetime.now() - \
                                 timedelta(minutes=
                                           int(self.posted_on
                                               .split()[0]))
                
            else:
                self.datefield = datetime.now() - \
                                 timedelta(hours=
                                           int(self.posted_on
                                               .split()[0]))
        super(NewsFeed, self).save(*args, **kwargs)
    """
    
    def __str__(self):
        return " " + str(self.url) + \
               " " + str(self.title) + \
               " " + str(self.hid)
    
    
class Profile(models.Model):
    """
    Profile is the model for a user's personalized details.
    Later editions, we may have a Profile picture.
    """
    id = models.AutoField(primary_key=True, auto_created=True)
    # Every User is supposed to own a unique profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, editable=True, blank=True)
    bday = models.DateField(editable=True, blank=True)
    email = models.EmailField(unique=True, max_length=100, blank=True)
    
    def get_absolute_url(self):
        return reverse('mainapp:profile', kwargs={'pk': self.id})
    
    def __str__(self):
        return str(self.id) + "--" + \
               str(self.user) + "--" + \
               str(self.name)
    

class Bookmarks(models.Model):
    """
    Bookmarks models is meant to keep a tab of
    all the bookmarks for the user.
    """
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    hack_id = models.ForeignKey(NewsFeed, on_delete=models.DO_NOTHING)
    bid = models.AutoField(primary_key=True, auto_created=True)
    
    
class UserRead(models.Model):
    """
    All the bookmarks deleted by the user.
    """
    userid = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    hid = models.ForeignKey(NewsFeed, on_delete=models.DO_NOTHING)
    read = models.BooleanField(default=True)
    dated = models.DateTimeField(auto_now_add=True)


class UserDeleted(models.Model):
    """
    UserDeleted: Hids that shouldn't be shown to the user.
    """
    userid = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    hid = models.ForeignKey(NewsFeed, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
