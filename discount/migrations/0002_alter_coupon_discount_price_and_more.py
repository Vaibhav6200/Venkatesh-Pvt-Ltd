# Generated by Django 4.2.5 on 2023-09-27 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='minimum_price',
            field=models.IntegerField(),
        ),
    ]