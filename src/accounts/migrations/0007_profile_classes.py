# Generated by Django 3.0.8 on 2020-07-18 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0012_auto_20200718_0243'),
        ('accounts', '0006_delete_subclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='classes',
            field=models.ManyToManyField(to='class.Class'),
        ),
    ]
