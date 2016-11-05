from django.db import models
from faker import Factory
from django.contrib.auth.models import User
# Create your models here.


class Article(models.Model):
    headline = models.CharField(null=True, blank=True, max_length=500)
    content = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)
    editors_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.headline


class Comment(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    comment = models.TextField(null=True)
    date = models.DateField(auto_now=True)
    belong_to = models.ForeignKey(to=Article, related_name='under_comments', null=True, blank=True)
    best_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.comment


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image')


class Ticket(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets')
    article = models.ForeignKey(to=Article, related_name='tickets')
    VOTE_CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('normal', 'normal'),

    )
    choice = models.CharField(choices=VOTE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)
# fake = Factory.create()
# for i in range(10):
#     v = Article(
#         headline=fake.text(max_nb_chars=90),
#         content=fake.text(max_nb_chars=3000),
#         )
#     v.save()
