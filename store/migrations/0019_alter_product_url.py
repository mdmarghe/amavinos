# Generated by Django 4.2.5 on 2023-10-01 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_product_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(default='https://google.com/'),
        ),
    ]
