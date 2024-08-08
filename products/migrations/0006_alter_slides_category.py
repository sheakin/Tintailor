# Generated by Django 5.0.6 on 2024-07-16 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_slides_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slides',
            name='category',
            field=models.CharField(choices=[('SB', 'Shirts And Blouses'), ('TS', 'T-Shirts'), ('trending', 'trending'), ('HS', 'Hoodies&Sweatshirts'), ('men', 'men'), ('women', 'women'), ('kids', 'kids'), ('sports', 'sports'), ('tailor', 'tailor')], default='women', max_length=100),
        ),
    ]