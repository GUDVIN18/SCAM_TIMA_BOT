# Generated by Django 5.1.1 on 2024-11-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0028_datausersite_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='datausersite',
            name='product_name',
            field=models.TextField(blank=True, help_text='Наименование товара', null=True),
        ),
    ]
