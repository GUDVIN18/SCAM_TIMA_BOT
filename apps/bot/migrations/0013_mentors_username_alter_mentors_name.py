# Generated by Django 5.1.1 on 2024-11-21 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0012_mentors'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentors',
            name='username',
            field=models.CharField(blank=True, help_text='@username', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mentors',
            name='name',
            field=models.CharField(blank=True, help_text='Имя', max_length=255, null=True),
        ),
    ]
