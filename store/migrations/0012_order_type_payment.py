# Generated by Django 3.0.5 on 2020-06-26 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20200625_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='type_payment',
            field=models.CharField(default='Cartao', max_length=50),
            preserve_default=False,
        ),
    ]
