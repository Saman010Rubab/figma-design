# Generated by Django 4.2.3 on 2024-07-29 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('figmapp', '0007_rename_images_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ads',
            new_name='Ad',
        ),
    ]
