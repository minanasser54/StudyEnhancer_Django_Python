# Generated by Django 3.0.8 on 2020-07-16 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0005_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
