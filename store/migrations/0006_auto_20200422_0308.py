# Generated by Django 3.0.5 on 2020-04-22 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200421_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproducts',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='store.Order'),
        ),
        migrations.DeleteModel(
            name='Client',
        ),
    ]
