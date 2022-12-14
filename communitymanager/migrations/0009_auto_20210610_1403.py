# Generated by Django 2.2.21 on 2021-06-10 14:03

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communitymanager', '0008_auto_20210610_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='vues',
            field=models.ManyToManyField(null=True, related_name='_post_vues_+', to=settings.AUTH_USER_MODEL, verbose_name='vus'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_evenement',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 10, 14, 3, 30, 254518), null=True),
        ),
    ]
