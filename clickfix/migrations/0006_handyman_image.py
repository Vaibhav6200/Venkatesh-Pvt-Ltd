# Generated by Django 4.2.5 on 2023-09-27 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickfix', '0005_alter_handyman_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='handyman',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='handyman'),
        ),
    ]
