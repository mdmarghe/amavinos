# Generated by Django 4.2.5 on 2023-09-21 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_vino_tipo_alter_vino_bodega_alter_vino_crianza_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cata',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]