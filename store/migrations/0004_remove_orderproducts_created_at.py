# Generated by Django 3.0.5 on 2020-04-21 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200421_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproducts',
            name='created_at',
        ),
    ]
