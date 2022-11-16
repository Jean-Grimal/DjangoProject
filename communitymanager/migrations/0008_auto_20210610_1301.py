# Generated by Django 2.2.21 on 2021-06-10 13:01

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0007_auto_20210610_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_evenement',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 10, 13, 1, 5, 737870), null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='_post_likes_+', to=settings.AUTH_USER_MODEL, verbose_name='likes'),
        ),
    ]