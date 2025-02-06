# Generated by Django 5.1.5 on 2025-02-04 12:46

import apps.users.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_profile_pic.jpg', null=True, storage=apps.users.storage.S3MediaStorage(), upload_to='profile_pictures/'),
        ),
    ]
