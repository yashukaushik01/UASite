# Generated by Django 3.2.2 on 2021-08-25 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_itinerarydata_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerarydata',
            name='end_extra_off',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
