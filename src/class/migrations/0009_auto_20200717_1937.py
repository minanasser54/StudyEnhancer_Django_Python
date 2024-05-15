# Generated by Django 3.0.8 on 2020-07-17 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('class', '0008_auto_20200716_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='class_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='class',
            name='tutor',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_tutor', to=settings.AUTH_USER_MODEL),
        ),
    ]
