# Generated by Django 3.1.1 on 2021-10-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0051_agent_agentproductbooking_agentwithdrawhistory_testimonials'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='margin_agent',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
