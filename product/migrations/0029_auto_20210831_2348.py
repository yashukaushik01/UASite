# Generated by Django 3.2.6 on 2021-08-31 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_locality'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelguide',
            name='blog16',
            field=models.CharField(blank=True, max_length=50000, null=True),
        ),
        migrations.AddField(
            model_name='travelguide',
            name='blog17',
            field=models.CharField(blank=True, max_length=50000, null=True),
        ),
        migrations.AddField(
            model_name='travelguide',
            name='blog18',
            field=models.CharField(blank=True, max_length=50000, null=True),
        ),
        migrations.AddField(
            model_name='travelguide',
            name='blog19',
            field=models.CharField(blank=True, max_length=50000, null=True),
        ),
        migrations.AddField(
            model_name='travelguide',
            name='blog20',
            field=models.CharField(blank=True, max_length=50000, null=True),
        ),
    ]