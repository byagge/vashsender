# Generated by Django 5.2.1 on 2025-06-08 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_remove_campaignstats_bounces_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtracking',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
