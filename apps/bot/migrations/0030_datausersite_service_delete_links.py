# Generated by Django 5.1.1 on 2024-11-29 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0029_datausersite_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='datausersite',
            name='service',
            field=models.CharField(blank=True, help_text='Название сервиса', max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Links',
        ),
    ]
