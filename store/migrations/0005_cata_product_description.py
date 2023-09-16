# Generated by Django 4.2.5 on 2023-09-16 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_category_id_alter_customer_id_alter_order_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cata',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.product')),
                ('data', models.DateTimeField()),
            ],
            bases=('store.product',),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
