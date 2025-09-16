# Переход на посты из таблицы и парсинг текста публикации, упоминаний других блогеров, ссылок из текста и скрытых упоминаний под "еще" или "и"

import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# Путь к chromedriver.exe
driver_path = r'C:\Users\sasha\OneDrive\Desktop\chromedriver.exe' 
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Авторизация вручную
driver.get("https://www.instagram.com/accounts/login/")
print("Авторизуйтесь вручную и нажмите Enter.")
input()

# Загрузка таблицы
input_file = 'instagram_collected_links.xlsx'
df = pd.read_excel(input_file)

# Подготовка колонок
for col in ['Текст публикации', 'Упоминания', 'Ссылки из блоков', 'Упомянутые аккаунты']:
    if col not in df.columns:
        df[col] = ''
    df[col] = df[col].astype(str)

# Исключения, запишите сюда профили создателей, в виде ссылок и ниже как юзеров
excluded_links = {
    'https://www.instagram.com/golomazdina',
    'https://www.instagram.com/12storeez',
    'https://www.instagram.com/ivan.kh',
}
excluded_mentions = {'@golomazdina', '@12storeez', '@ivan.kh'}

# Основной цикл
for idx, row in df.iterrows():
    url = row['Post Links']
    driver.get(url)
    time.sleep(3)

    # 1. Текст публикации
    try:
        text_elem = driver.find_element(By.XPATH, "//h1[contains(@class, '_ap3a')]")
        post_text = text_elem.text
    except NoSuchElementException:
        post_text = "Нет текста"

    # 2. Упоминания через @ (с фильтром)
    mentions = re.findall(r'@[\w._]+', post_text)
    mentions = [m for m in mentions if m.lower() not in excluded_mentions]

    # 3. Основные ссылки из <a class="_acan">
    account_links = set()
    try:
        blocks = driver.find_elements(By.XPATH, '//a[contains(@class, "_acan") and contains(@href, "/")]')
        for block in blocks:
            href = block.get_attribute('href')
            if href and 'instagram.com' in href:
                account_links.add(href.rstrip('/'))
    except Exception:
        pass

    # 4. Работа с "ещё" и "и"
    mentioned_accounts = set()
    try:
        span_blocks = driver.find_elements(By.XPATH, '//span[@style="line-height: 18px;"]')
        for span in span_blocks:
            span_text = span.text.strip().lower()

            if 'ещё' in span_text:
                try:
                    link_inside = span.find_element(By.XPATH, './/a')
                    driver.execute_script("arguments[0].click();", link_inside)
                except NoSuchElementException:
                    driver.execute_script("arguments[0].click();", span)
                time.sleep(1.5)

            elif 'и' in span_text:
                try:
                    links_in_span = span.find_elements(By.XPATH, './/a')
                    for link in links_in_span:
                        href = link.get_attribute('href')
                        if href and 'instagram.com' in href:
                            mentioned_accounts.add(href.rstrip('/'))
                except NoSuchElementException:
                    continue
    except Exception:
        pass

    # 5. Дополнительные <a> после раскрытия списка
    try:
        all_links = driver.find_elements(By.XPATH, '//span[@style="line-height: 18px;"]//a')
        for link in all_links:
            href = link.get_attribute('href')
            if href and 'instagram.com' in href:
                mentioned_accounts.add(href.rstrip('/'))
    except Exception:
        pass

    # Фильтрация: исключения и ссылки на посты (/p/)
    account_links = {link for link in account_links if link not in excluded_links}
    mentioned_accounts = {
        link for link in mentioned_accounts
        if link not in excluded_links and '/p/' not in link
    }

    # 6. Сохраняем
    df.at[idx, 'Текст публикации'] = post_text
    df.at[idx, 'Упоминания'] = ', '.join(sorted(set(mentions)))
    df.at[idx, 'Ссылки из блоков'] = ', '.join(sorted(account_links))
    df.at[idx, 'Упомянутые аккаунты'] = ', '.join(sorted(mentioned_accounts))

    print(f"[{idx + 1}/{len(df)}] Пост обработан.")
    print(f"{mentions}")
    print(f"{account_links}")
    print(f"{mentioned_accounts}")

# Сохраняем результат
df.to_excel('instagram_parsed_results_FINAL.xlsx', index=False)
print("\n Парсинг завершён. Данные сохранены в 'instagram_parsed_results_FINAL.xlsx'")

# Закрываем драйвер
driver.quit()

