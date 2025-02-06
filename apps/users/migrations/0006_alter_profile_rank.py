# Generated by Django 5.1.5 on 2025-02-03 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_infinite_flight_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rank',
            field=models.CharField(choices=[('Membership Pending', 'Membership Pending'), ('Cadet Under Review', 'Cadet Under Review'), ('Cadet', 'Cadet'), ('Second Officer', 'Second Officer'), ('First Officer Under Review', 'First Officer Under Review'), ('First Officer', 'First Officer')], default='Membership Pending', max_length=50),
        ),
    ]
