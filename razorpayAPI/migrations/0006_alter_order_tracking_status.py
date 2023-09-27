# Generated by Django 4.2.5 on 2023-09-27 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('razorpayAPI', '0005_alter_order_tracking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tracking_status',
            field=models.IntegerField(blank=True, choices=[(1, 'Booked Today'), (2, 'Out For Service'), (3, 'Service Begun'), (4, 'Service Completed')], null=True),
        ),
    ]