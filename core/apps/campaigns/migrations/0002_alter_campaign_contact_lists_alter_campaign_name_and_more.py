# Generated by Django 5.2.1 on 2025-05-28 03:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
        ('emails', '0007_remove_senderemail_updated_at_and_more'),
        ('mail_templates', '0001_initial'),
        ('mailer', '0002_alter_contact_options_alter_contactlist_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='contact_lists',
            field=models.ManyToManyField(blank=True, related_name='campaigns', to='mailer.contactlist'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='reply_to',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_email',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='emails.senderemail'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='sender_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='subject',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mail_templates.emailtemplate'),
        ),
    ]
