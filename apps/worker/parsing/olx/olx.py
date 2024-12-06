import os
import requests
from bs4 import BeautifulSoup
# from bot_builder.settings import MEDIA_ROOT
MEDIA_ROOT = 'media'


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


            prices = soup.find('h3', class_='css-uhl2ga').text
            print(prices)
            

            product_name = soup.find('h4', class_='css-11nsr42').text
            print(product_name)


            images = soup.find_all('div', class_='swiper-zoom-container')
            for i, img in enumerate(images, start=1):
                img_tag = img.find('img', class_='css-1bmvjcs')
                src = img_tag.get('src')
                if src and i == 1:
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
                

            return product_name, prices, relative_file_path 

        except requests.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return 0

# # Примеры использования
# def main():
#     url = 'https://www.olx.ro/d/oferta/pret-fix-dji-avata-2-fly-more-combo-sigilata-3-baterii-cititi-anuntul-IDipV0k.html'
#     folder = "olx"
#     parser = WebsiteParser(url, folder, user_tg_id=999)
#     a = parser.parse_and_save_images()
#     print('out', a)

# if __name__ == '__main__':
#     main()