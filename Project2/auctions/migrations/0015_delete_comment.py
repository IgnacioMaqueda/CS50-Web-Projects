# Generated by Django 4.1.7 on 2023-03-02 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listing_closed'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
