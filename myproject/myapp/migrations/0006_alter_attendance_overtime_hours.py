# Generated by Django 5.1.4 on 2025-02-18 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_payment_total_billed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='overtime_hours',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
