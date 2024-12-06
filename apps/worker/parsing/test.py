import undetected_chromedriver.v2 as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Настройки для работы в фоновом режиме
options = Options()
options.add_argument('--headless')  # Фоновый режим
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Указываем путь к chromedriver
service = Service('/usr/local/bin/chromedriver')

# Инициализация WebDriver с undetected_chromedriver
driver = uc.Chrome(service=service, options=options)

# Открываем URL
url = "https://wallapopp.rosebuc.shop/get/63HK39MD52W39/"
driver.get(url)

# Получаем HTML контент страницы
html_content = driver.page_source

# Сохраняем HTML в файл (если нужно)
with open("page_content.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# Закрываем драйвер
driver.quit()
