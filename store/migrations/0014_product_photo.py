# Generated by Django 3.0.5 on 2020-06-29 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='asdasd', upload_to='images/'),
            preserve_default=False,
        ),
    ]
