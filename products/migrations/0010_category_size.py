# Generated by Django 5.0.6 on 2024-07-28 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_order_orderitem_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='size',
            field=models.CharField(default='exit', max_length=50),
            preserve_default=False,
        ),
    ]