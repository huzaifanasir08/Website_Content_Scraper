# Generated by Django 5.1.3 on 2025-01-18 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping_task', '0006_flightschoolwebsfetcheddata_content_length_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightschoolwebsfetcheddata',
            name='content',
        ),
    ]
