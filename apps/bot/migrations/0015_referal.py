# Generated by Django 5.1.1 on 2024-11-21 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_alter_botuser_has_mentor_profit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_invite', models.ForeignKey(blank=True, help_text='Кто пришел', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ref_user_invite', to='bot.botuser', verbose_name='Кто перешел')),
                ('user_main', models.ForeignKey(blank=True, help_text='Отправитель', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ref_user_main', to='bot.botuser', verbose_name='Отправитель')),
            ],
        ),
    ]
