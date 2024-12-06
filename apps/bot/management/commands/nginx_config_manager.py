
# yourapp/management/commands/nginx_config_manager.py
import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.bot.models import Country_Sites  # Замените на ваш реальный путь к модели

class NginxConfigManager:
    def __init__(self, 
                 server_ip='146.19.128.6',
                 proxy_port='8091'):
        self.server_ip = server_ip
        self.proxy_port = proxy_port
        
        # Основные пути nginx
        self.nginx_sites_available = '/etc/nginx/sites-available'
        self.nginx_sites_enabled = '/etc/nginx/sites-enabled'
        
        # Имя файла с общей конфигурацией доменов
        self.domains_config_filename = 'dynamic_domains'

    def _generate_nginx_config(self, domains):
        """
        Генерация полной конфигурации nginx для всех доменов
        """
        config = "# Автоматически сгенерированная конфигурация\n"
        for domain_name in domains:
            config += f'''server {{
    listen 80;
    server_name {domain_name};

    location / {{
        proxy_pass http://{self.server_ip}:{self.proxy_port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
'''
        return config

    def update_nginx_config(self, domains):
        """
        Полное обновление конфигурации nginx
        """
        try:
            # Полный путь к файлу конфигурации
            config_file_path = os.path.join(
                self.nginx_sites_available, 
                self.domains_config_filename
            )
            
            # Создаем/перезаписываем файл полностью
            with open(config_file_path, 'w') as f:
                f.write(self._generate_nginx_config(domains))
            
            # Создаем симлинк в sites-enabled
            symlink_path = os.path.join(
                self.nginx_sites_enabled, 
                self.domains_config_filename
            )
            
            # Удаляем старый симлинк, если существует
            if os.path.exists(symlink_path):
                os.unlink(symlink_path)
            
            # Создаем новый симлинк
            os.symlink(config_file_path, symlink_path)
            
            return True
        
        except Exception as e:
            print(f"Ошибка подготовки конфигурации: {e}")
            return False



class Command(BaseCommand):
    help = 'Обновление конфигурации nginx для всех активных доменов'

    def add_arguments(self, parser):
        """
        Добавляем необязательные аргументы
        """
        parser.add_argument(
            '--restart', 
            action='store_true', 
            help='Перезапустить nginx после обновления'
        )

    def handle(self, *args, **options):
        # Получаем все активные домены
        active_domains = Country_Sites.objects.filter(is_active=True).values_list('url', flat=True)
        
        if not active_domains:
            self.stdout.write(self.style.WARNING('Нет активных доменов'))
            return
        
        # Инициализируем менеджер
        nginx_manager = NginxConfigManager()
        
        # Обновляем конфигурацию
        success = nginx_manager.update_nginx_config(active_domains)
        
        if success:
            self.stdout.write(self.style.SUCCESS(f'Конфигурация nginx обновлена для {len(active_domains)} доменов'))
            
            # Опциональный рестарт nginx
            if options['restart']:
                try:
                    subprocess.run(['systemctl', 'restart', 'nginx'], check=True)
                    self.stdout.write(self.style.SUCCESS('Nginx перезапущен'))
                except subprocess.CalledProcessError:
                    self.stdout.write(self.style.ERROR('Не удалось перезапустить nginx'))
        else:
            self.stdout.write(self.style.ERROR('Не удалось обновить конфигурацию nginx'))