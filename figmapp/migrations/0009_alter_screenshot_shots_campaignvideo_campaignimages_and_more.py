# Generated by Django 4.2.3 on 2024-07-29 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('figmapp', '0008_rename_ads_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenshot',
            name='shots',
            field=models.ImageField(null=True, upload_to='campaign/images'),
        ),
        migrations.CreateModel(
            name='CampaignVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videos', models.FileField(null=True, upload_to='campaign/videos')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='figmapp.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(null=True, upload_to='campaign/images')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='figmapp.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(null=True, upload_to='campaign/files')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='figmapp.campaign')),
            ],
        ),
    ]
