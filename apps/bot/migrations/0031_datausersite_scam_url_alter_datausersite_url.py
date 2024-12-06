# Generated by Django 5.1.1 on 2024-11-29 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0030_datausersite_service_delete_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='datausersite',
            name='scam_url',
            field=models.URLField(blank=True, help_text='Скам ссылка', null=True),
        ),
        migrations.AlterField(
            model_name='datausersite',
            name='url',
            field=models.URLField(blank=True, help_text='Ориг. ссылка', null=True),
        ),
    ]
