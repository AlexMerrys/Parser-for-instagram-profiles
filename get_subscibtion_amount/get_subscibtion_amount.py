# Сбор подписчиков на акканте с помощью цикличного перехода по ним из ссылок в таблице "links" и сохранение в instagram_followers_result

import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Настрой путь к chromedriver
driver_path = r'C:\Users\sasha\OneDrive\Desktop\chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Авторизация вручную
driver.get("https://www.instagram.com/accounts/login/")
print("Авторизуйтесь вручную и нажмите Enter.")
input()

# Загрузка Excel с аккаунтами
input_file = r'C:\Users\sasha\PycharmProjects\parser3\links.xlsx'
df = pd.read_excel(input_file)

# Создаём колонку для подписчиков
if 'Подписчики' not in df.columns:
    df['Подписчики'] = ''

# Цикл по аккаунтам
for idx, row in df.iterrows():
    url = row['links']
    driver.get(url)
    time.sleep(2)

    followers = "Мало слишком"

    try:
        # Получаем все <span>, в которых может быть инфа о подписчиках
        spans = driver.find_elements(By.XPATH, '//span[contains(text(), "тыс.") or contains(text(), "млн")]')
        for span in spans:
            text = span.text.replace('\xa0', ' ').strip()
            match = re.match(r'([\d.,]+)\s?(тыс\.|млн)', text.lower())
            if match:
                number, multiplier = match.groups()
                number = float(number.replace(',', '.'))
                if multiplier == 'тыс.':
                    number *= 1_000
                elif multiplier == 'млн':
                    number *= 1_000_000
                followers = int(number)
                break
    except NoSuchElementException:
        followers = "Ошибка"

    df.at[idx, 'Подписчики'] = followers
    print(f"[{idx + 1}/{len(df)}] {url} — {followers}")

# Сохраняем результат
output_file = r'C:\Users\sasha\PycharmProjects\parser3\instagram_followers_result.xlsx'
df.to_excel(output_file, index=False)

print(f"\n Готово! Сохранено в файл: {output_file}")

# Закрыть браузер

driver.quit()
