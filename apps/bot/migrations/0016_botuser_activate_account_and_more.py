# Generated by Django 5.1.1 on 2024-11-21 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0015_referal'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='activate_account',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='botuser',
            name='total_profit_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True, verbose_name='Общая сумма профитов (USD)'),
        ),
        migrations.AlterField(
            model_name='botuser',
            name='total_profit_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Общее количество профитов'),
        ),
    ]
