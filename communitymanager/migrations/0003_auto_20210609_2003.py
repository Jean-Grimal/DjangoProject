# Generated by Django 2.2.21 on 2021-06-09 20:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0002_post_titre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_evenement',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 9, 20, 3, 33, 961563), null=True),
        ),
    ]