from django.contrib import admin
from tenMinutesApp.models import Article, Comment, UserProfile, Ticket


admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Ticket)
