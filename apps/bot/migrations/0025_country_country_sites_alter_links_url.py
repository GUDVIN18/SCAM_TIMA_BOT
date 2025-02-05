# Generated by Django 5.1.1 on 2024-11-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0024_links_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Название страны', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Страну',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Country_Sites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Название Сайта', max_length=255, null=True)),
                ('url', models.URLField(blank=True, help_text='Введите URL-адрес', max_length=555, null=True)),
            ],
            options={
                'verbose_name': 'Страну',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.AlterField(
            model_name='links',
            name='url',
            field=models.URLField(blank=True, help_text='URL-адрес', max_length=555, null=True),
        ),
    ]
