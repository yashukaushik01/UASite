# Generated by Django 3.2.6 on 2021-10-07 13:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0041_purchase_margin'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliateuser',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]