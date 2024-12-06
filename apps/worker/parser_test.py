from playwright.sync_api import sync_playwright

def parse_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        html = page.content()
        
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print("Страница успешно загружена")
        browser.close()
        return html

# Пример использования
url = "https://vinted-it.pebal.shop/get/90XX25WI07Y73/"
parse_with_playwright(url)