# Generated by Django 2.2.6 on 2019-10-03 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views_count',
            field=models.IntegerField(default=0),
        ),
    ]
