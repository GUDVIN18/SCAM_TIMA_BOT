# Generated by Django 5.1.1 on 2024-11-21 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0018_links_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='url',
            field=models.TextField(blank=True, help_text='URL', null=True),
        ),
    ]
