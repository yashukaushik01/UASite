# Generated by Django 3.1.1 on 2021-11-11 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0065_auto_20211111_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='number_of_adults',
            field=models.CharField(blank=True, default=None, max_length=122, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='number_of_child',
            field=models.CharField(blank=True, default=None, max_length=122, null=True),
        ),
    ]
