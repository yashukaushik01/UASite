# Generated by Django 3.2.6 on 2021-08-30 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_cities_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerarydata',
            name='end_extra_off',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
