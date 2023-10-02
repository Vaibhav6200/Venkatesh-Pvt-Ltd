# Generated by Django 4.2.5 on 2023-10-02 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickfix', '0006_alter_deals_and_discount_heading_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deals_and_discount',
            name='subheading',
        ),
        migrations.AddField(
            model_name='deals_and_discount',
            name='description',
            field=models.CharField(blank=True, help_text='it can be at max 256 of characters long', max_length=255, null=True),
        ),
    ]
