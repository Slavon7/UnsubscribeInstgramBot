from playwright.sync_api import sync_playwright
import time

def fetch_float_and_paint_seed():
    with sync_playwright() as p:
        # Укажите путь к папке с расширением
        extension_dir = "C:/Users/Viacheslav/Documents/CSFloatMarketChecker"

        # Настраиваем аргументы для загрузки расширения
        print("Запускаем браузер с расширением...")
        browser = p.firefox.launch_persistent_context(
            user_data_dir="C:/Users/Viacheslav/Documents/playwright_data",
            headless=False,
            args=[f"--disable-extensions-except={extension_dir}", f"--load-extension={extension_dir}"]
        )

        # Создаем новую страницу и переходим на нужный сайт
        print("Создаем новую страницу...")
        page = browser.new_page()
        print("Переход на сайт...")
        page.goto("https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Alpine%20Camo%20(Minimal%20Wear)")

        # Ожидаем, пока страница полностью загрузится
        page.wait_for_load_state("networkidle")
        time.sleep(5)

        # Ожидаем загрузку элемента csfloat-item-row-wrapper
        try:
            # Ожидаем, пока элемент csfloat-item_row-wrapper будет виден
            item_row_wrapper = page.wait_for_selector('csfloat-item-row-wrapper', timeout=30000)

            # Ожидаем небольшую задержку, чтобы дать время для загрузки теневого дерева
            page.wait_for_timeout(1000)

            # Проверка наличия теневого корня и данных
            float_data = item_row_wrapper.evaluate('el => { \
                const shadowRoot = el.shadowRoot; \
                if (shadowRoot) { \
                    const floatRow = shadowRoot.querySelector(".float-row-wrapper"); \
                    return floatRow ? floatRow.innerText : null; \
                } \
                return null; \
            }')

            if float_data is None:
                print("Ошибка: данные float не найдены в теневом дереве.")
                return

            # Разделение данных на Float и Paint Seed
            float_value = float_data.split("Float: ")[1].split("\n")[0].strip()
            paint_seed_value = float_data.split("Paint Seed: ")[1].strip()

            print(f"Float: {float_value}")
            print(f"Paint Seed: {paint_seed_value}")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            browser.close()

# Запуск функции
fetch_float_and_paint_seed()
