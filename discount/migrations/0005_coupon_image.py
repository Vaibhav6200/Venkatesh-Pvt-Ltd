# Generated by Django 4.2.5 on 2023-09-27 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0004_alter_coupon_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='coupon_images'),
        ),
    ]
