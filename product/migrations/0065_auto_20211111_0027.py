# Generated by Django 3.1.1 on 2021-11-11 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0064_auto_20211107_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='booking_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
