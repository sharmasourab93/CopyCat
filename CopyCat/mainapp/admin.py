from django.contrib import admin
from .models import NewsFeed, Bookmarks, Profile, UserRead, UserDeleted


admin.site.register(NewsFeed)
admin.site.register(Profile)
admin.site.register(Bookmarks)
admin.site.register(UserRead)
admin.site.register(UserDeleted)


