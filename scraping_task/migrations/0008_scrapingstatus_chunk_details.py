# Generated by Django 5.1.3 on 2025-01-25 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping_task', '0007_remove_flightschoolwebsfetcheddata_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapingstatus',
            name='chunk_details',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
