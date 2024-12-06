# Generated by Django 5.1.1 on 2024-11-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_remove_botuser_login_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Тип кнопки', max_length=255)),
                ('desciptions', models.TextField(blank=True, help_text='Описание', null=True)),
            ],
            options={
                'verbose_name': 'Наставника',
                'verbose_name_plural': 'Наставники',
            },
        ),
    ]
