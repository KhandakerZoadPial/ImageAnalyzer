# Generated by Django 4.1.5 on 2023-01-30 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
