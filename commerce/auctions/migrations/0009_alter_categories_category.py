# Generated by Django 5.0.1 on 2024-02-01 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_categories_category_categories_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category',
            field=models.CharField(choices=[('Antiques', 'Antiques'), ('Art & Decor', 'Art'), ('Books', 'Books'), ('CD, DVD & Games', 'Games'), ('Clothing & Fasion', 'Clothing'), ('Collectables', 'Collectables'), ('Computers', 'Computers'), ('Dining', 'Dining'), ('Electronics & Gadgets', 'Electronics'), ('Handbags', 'Handbags'), ('Lawn & Garden', 'Lawn'), ('Sports & Equipment', 'Sports'), ('Toys', 'Toys'), ('Travel Accesaries', 'Travel')], max_length=30, null=True),
        ),
    ]
