# Generated by Django 4.2.5 on 2023-10-14 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickfix', '0012_bookcall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcall',
            name='duration',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='bookcall',
            name='quantity',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]