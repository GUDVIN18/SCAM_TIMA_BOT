# Generated by Django 5.1.1 on 2024-12-03 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0035_botuser_token_temporary'),
    ]

    operations = [
        migrations.AddField(
            model_name='datausersite',
            name='support_json',
            field=models.JSONField(blank=True, help_text='json поддержки', null=True),
        ),
        migrations.AlterField(
            model_name='datausersite',
            name='data_json',
            field=models.JSONField(blank=True, help_text='json для кнопок', null=True),
        ),
    ]
