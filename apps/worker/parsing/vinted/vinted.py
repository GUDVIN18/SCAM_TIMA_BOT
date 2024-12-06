import os
import requests
from bs4 import BeautifulSoup
from bot_builder.settings import MEDIA_ROOT
# MEDIA_ROOT = 'media'


class WebsiteParser:
    def __init__(self, url, username, password, proxy_host, proxy_port, folder, user_tg_id):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.username = username
        self.password = password
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.folder = folder
        self.user_tg_id = user_tg_id

    def parse_and_save_images(self,):
        folder_name = self.folder
        try:
            folder_path = os.path.join("media", folder_name)

            # Создаем папку, если она не существует
            os.makedirs(folder_path, exist_ok=True)

            proxies = {
                'http': f'http://{self.username}:{self.password}@{self.proxy_host}:{self.proxy_port}',
                'https': f'http://{self.username}:{self.password}@{self.proxy_host}:{self.proxy_port}',
            } if self.proxy_host else None

            print('proxy:', proxies)

            # Отправляем GET-запрос на страницу
            response = requests.get(
                self.url, 
                headers=self.headers, 
                proxies=proxies,
                timeout=10  # Добавляем таймаут
            )
            response.raise_for_status()

            # Создаем объект BeautifulSoup для парсинга
            soup = BeautifulSoup(response.text, 'html.parser')

            images = soup.find_all('figure', class_='item-description u-flexbox item-photo item-photo--1')

            prices = soup.find_all('div', class_='box box--item-details u-border-radius-inherit')
            for price in prices:
                price_total = price.find('div', class_='web_ui__Text__text web_ui__Text__title web_ui__Text__left web_ui__Text__clickable web_ui__Text__underline-none').text
                print(price_total)

            product_names = soup.find_all('span', class_='web_ui__Text__text web_ui__Text__title web_ui__Text__left')

            for product in product_names:
                product_name = product.get_text(strip=True)  # Извлекаем текст и убираем лишние пробелы
                print(product_name)


            for i, img in enumerate(images, start=1):
                img_tag = img.find('img', class_='web_ui__Image__content')
                src = img_tag.get('src')
                print('src', src)
                if src:
                    try:
                        # Загружаем изображение через тот же прокси
                        img_response = requests.get(
                            src, 
                            headers=self.headers, 
                            proxies=proxies,
                            timeout=10
                        )
                        img_response.raise_for_status()

                        # Формируем путь к файлу
                        file_path = os.path.join(folder_path, f'image_{self.user_tg_id}.jpg')

                        # Сохраняем изображение
                        with open(file_path, 'wb') as f:
                            f.write(img_response.content)
                        print(f'Изображение {i} сохранено в {file_path}')

                        relative_file_path = os.path.relpath(file_path, MEDIA_ROOT)

                    except requests.RequestException as e:
                        print(f"Ошибка при сохранении изображения {i}: {e}")
                

            return product_name, price_total, relative_file_path 

        except requests.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return 0

# # Примеры использования
# def main():
#     url = 'https://www.vinted.it/items/5458039023-maracazzani-vintage-bellissimo-gilet-da-donna-tglxl?homepage_session_id=d2bbf573-f845-40a0-bad7-ffd55d930d9a'
#     username = "v5Hxfz"
#     password = "w5QNqr"
#     proxy_host = "45.91.209.157"
#     proxy_port = "12071"
#     folder = "vinted"
#     parser = WebsiteParser(url, username, password, proxy_host, proxy_port, folder)
#     a = parser.parse_and_save_images()
#     print('out', a)

# if __name__ == '__main__':
#     main()