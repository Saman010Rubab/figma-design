# Generated by Django 4.2.3 on 2024-07-30 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('figmapp', '0009_alter_screenshot_shots_campaignvideo_campaignimages_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(null=True, upload_to='campaign/images')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='figmapp.campaign')),
            ],
        ),
        migrations.RenameModel(
            old_name='CampaignFiles',
            new_name='CampaignFile',
        ),
        migrations.DeleteModel(
            name='CampaignImages',
        ),
    ]
