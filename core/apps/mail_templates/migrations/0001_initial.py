# Generated by Django 5.2.1 on 2025-05-26 03:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Название шаблона', max_length=200)),
                ('html_content', models.TextField(help_text='HTML-контент, используется для рендеринга письма')),
                ('ck_content', models.TextField(blank=True, help_text='Исходный контент из CKEditor (если нужен отдельно)')),
                ('plain_text_content', models.TextField(blank=True, help_text='Текстовая версия письма без HTML')),
                ('is_draft', models.BooleanField(default=True, help_text='Шаблон сохраняется как черновик')),
                ('send_count', models.PositiveIntegerField(default=0, help_text='Сколько раз использован для рассылки')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Когда шаблон создан')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Когда последний раз сохранялся')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_templates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Email шаблон',
                'verbose_name_plural': 'Email шаблоны',
                'ordering': ['-updated_at'],
                'unique_together': {('owner', 'title')},
            },
        ),
    ]
