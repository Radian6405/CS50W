# Generated by Django 5.0.1 on 2024-02-01 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_categories_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category',
            field=models.CharField(choices=[('AN', 'Antiques'), ('AR', 'Art & Decor'), ('BO', 'Books'), ('CD', 'CD, DVD & Games'), ('CL', 'Clothing & Fasion'), ('CO', 'Collectables'), ('CM', 'Computers'), ('DI', 'Dining'), ('EL', 'Electronics & Gadgets'), ('HA', 'Handbags'), ('LA', 'Lawn & Garden'), ('SP', 'Sports & Equipment'), ('TO', 'Toys'), ('TR', 'Travel Accesaries')], max_length=2, null=True),
        ),
    ]
