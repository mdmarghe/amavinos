# Generated by Django 4.2.5 on 2023-09-16 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_data_cata_date_cata_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='cata',
            name='location',
            field=models.CharField(default='Calle Antillano Campos, 5', max_length=50),
        ),
    ]