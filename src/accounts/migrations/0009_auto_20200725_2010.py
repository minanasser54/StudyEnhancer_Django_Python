# Generated by Django 3.0.8 on 2020-07-25 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0018_auto_20200724_1855'),
        ('accounts', '0008_auto_20200724_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='classes',
            field=models.ManyToManyField(blank=True, to='class.Class'),
        ),
    ]