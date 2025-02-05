# Generated by Django 5.1.1 on 2024-12-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0037_domain'),
    ]

    operations = [
        migrations.RenameField(
            model_name='domain',
            old_name='domain',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='domain',
            name='target_port',
        ),
        migrations.AddField(
            model_name='domain',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domain',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
