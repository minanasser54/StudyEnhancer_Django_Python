# Generated by Django 3.0.8 on 2020-07-16 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0006_lesson_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='url1',
            new_name='vid1',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='url2',
            new_name='vid2',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='url3',
            new_name='vid3',
        ),
    ]