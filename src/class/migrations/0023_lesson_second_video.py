# Generated by Django 3.0.8 on 2020-09-06 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0022_lesson_main_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='second_video',
            field=models.FileField(blank=True, null=True, upload_to='lesson_videos/'),
        ),
    ]