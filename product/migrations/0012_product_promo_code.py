# Generated by Django 3.2.2 on 2021-08-12 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_productenquiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='promo_code',
            field=models.CharField(default='AU', max_length=100),
        ),
    ]
