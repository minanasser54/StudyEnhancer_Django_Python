# Generated by Django 3.0.8 on 2020-09-19 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0024_lesson_third_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
    ]
