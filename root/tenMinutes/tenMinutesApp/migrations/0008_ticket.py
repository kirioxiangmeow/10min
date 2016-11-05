# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenMinutesApp', '0007_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(choices=[('like', 'like'), ('dislike', 'dislike'), ('normal', 'normal')], max_length=10)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='tenMinutesApp.Article')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted_tickets', to='tenMinutesApp.UserProfile')),
            ],
        ),
    ]
