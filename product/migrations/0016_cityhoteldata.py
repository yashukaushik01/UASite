# Generated by Django 3.2.2 on 2021-08-17 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_stateitinerarydata'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityHotelData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('accommodation_category', models.CharField(blank=True, max_length=200, null=True)),
                ('stay_name', models.CharField(blank=True, max_length=500, null=True)),
                ('room_type', models.CharField(blank=True, max_length=500, null=True)),
                ('meal_type', models.CharField(blank=True, max_length=500, null=True)),
                ('room_sharing', models.CharField(blank=True, max_length=500, null=True)),
                ('honeymoon_kit_price', models.IntegerField(blank=True, null=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('hotel_link', models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]