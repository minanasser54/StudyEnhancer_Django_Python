# Generated by Django 3.0.8 on 2020-07-25 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0018_auto_20200724_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainsubject',
            name='main_book',
        ),
    ]