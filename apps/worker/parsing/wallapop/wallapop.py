import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bot_builder.settings import MEDIA_ROOT
# MEDIA_ROOT = 'media'


class WebsiteParser:
    def __init__(self, url, folder, user_tg_id):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.folder = folder
        self.user_tg_id = user_tg_id

    def parse_and_save_images(self,):
        folder_name = self.folder
        try:
            folder_path = os.path.join("media", folder_name)

            # Создаем папку, если она не существует
            os.makedirs(folder_path, exist_ok=True)

            # Отправляем GET-запрос на страницу
            response = requests.get(
                self.url, 
                headers=self.headers, 
                timeout=10  # Добавляем таймаут
            )
            response.raise_for_status()

            # Создаем объект BeautifulSoup для парсинга
            soup = BeautifulSoup(response.text, 'html.parser')

            prices = soup.find_all('div', class_='d-flex justify-content-between')
            print('prices',prices)

            for price in prices:
                price_total = price.find('span', class_='item-detail-price_ItemDetailPrice--standard__TxPXr').text
                print(price_total)


            product_names = soup.find_all('h1', class_='item-detail_ItemDetail__title__wcPRl mt-2')
            for product in product_names:
                product_name = product.get_text(strip=True)  # Извлекаем текст и убираем лишние пробелы
                print(product_name)







            options = Options()
            options.add_argument('--headless')  # Фоновый режим
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            # Используем chromedriver
            driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'), options=options)


            # Открытие страницы
            driver.get(self.url)

            # Получение HTML-кода страницы после рендеринга JavaScript
            html_driver = driver.page_source

            # Создание объекта BeautifulSoup
            soup_driver = BeautifulSoup(html_driver, 'html.parser')

            # Извлечение изображений
            images = soup_driver.find_all('img', {'slot': 'carousel-content'})
            for i, img in enumerate(images):
                src = (img['src'])
                if i == 0:
                    if src:
                        try:
                            # Загружаем изображение через тот же прокси
                            img_response = requests.get(
                                src, 
                                headers=self.headers, 
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
            driver.quit()


            return product_name, price_total, relative_file_path 

        except requests.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return 0

# # Примеры использования
# def main():
#     url = 'https://it.wallapop.com/item/tabla-snowboard-nitro-t1-2023-2024-1072387295'
#     folder = "Wallapop"
#     user_tg_id = "34343434"
#     parser = WebsiteParser(url, folder, user_tg_id)
#     a = parser.parse_and_save_images()
#     print('out', a)

# if __name__ == '__main__':
#     main()