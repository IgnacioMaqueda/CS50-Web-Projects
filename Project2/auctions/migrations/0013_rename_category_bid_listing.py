# Generated by Django 4.1.7 on 2023-03-01 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_bids_alter_bid_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='category',
            new_name='listing',
        ),
    ]
