# Generated by Django 2.0 on 2018-10-16 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='location',
            field=models.CharField(max_length=3),
        ),
    ]
