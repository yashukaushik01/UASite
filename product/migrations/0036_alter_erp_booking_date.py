# Generated by Django 3.2.6 on 2021-09-30 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0035_erp_booking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='erp',
            name='booking_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
