# Generated by Django 5.1.5 on 2025-02-03 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_rank_alter_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='infinite_flight_username',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
