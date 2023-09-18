# Generated by Django 4.2.5 on 2023-09-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_cata_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='cata',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
