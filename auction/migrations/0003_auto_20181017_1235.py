# Generated by Django 2.1.2 on 2018-10-17 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_auction_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
