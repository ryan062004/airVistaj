# Generated by Django 5.1.5 on 2025-02-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rank',
            field=models.CharField(default='Membership Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(default='Pilot', max_length=100),
        ),
    ]
