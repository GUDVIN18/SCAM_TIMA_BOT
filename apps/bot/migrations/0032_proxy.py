# Generated by Django 5.1.1 on 2024-11-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0031_datausersite_scam_url_alter_datausersite_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('proxy_host', models.CharField(max_length=255)),
                ('proxy_port', models.CharField(max_length=255)),
            ],
        ),
    ]
