# Generated by Django 3.2.6 on 2021-09-28 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_affiliateuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliateuser',
            name='aid',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
