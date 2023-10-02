# Generated by Django 4.2.5 on 2023-10-02 06:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickfix', '0004_deals_and_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deals_and_discount',
            options={'verbose_name_plural': 'Deals & Discount'},
        ),
        migrations.AddField(
            model_name='deals_and_discount',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 10, 2, 6, 3, 49, 626718, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deals_and_discount',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]