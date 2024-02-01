# Generated by Django 5.0.1 on 2024-01-31 16:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctionlisting_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='WinListings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.PositiveSmallIntegerField(choices=[(1, 'Antiques'), (2, 'Art & Decor'), (3, 'Books'), (4, 'CD, DVD & Games'), (5, 'Clothing & Fasion'), (6, 'Collectables'), (7, 'Computers'), (8, 'Dining'), (9, 'Electronics & Gadgets'), (10, 'Handbags'), (11, 'Lawn & Garden'), (12, 'Sports & Equipment'), (13, 'Toys'), (14, 'Travel Accesaries')], null=True)),
                ('listing', models.ManyToManyField(blank=True, related_name='Category', to='auctions.auctionlisting')),
            ],
        ),
    ]