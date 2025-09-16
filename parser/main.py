import pyautogui as pag 
import pyperclip
import pandas as pd
import time
import keyboard

pag.FAILSAFE = False
pag.PAUSE = 0.3

all_links = []

print("Запущено. Нажмите F1, чтобы остановить в любой момент.\n")

for i in range(2):
    if keyboard.is_pressed('F1'):
        print("\n🛑 Остановка по F1!")
        break

    # 🔎 Проверка текущего URL
    pag.click(301, 63, button='right')
    time.sleep(0.2)
    pag.click(380, 256, button='left')
    time.sleep(0.2)
    current_url = pyperclip.paste().strip()

    if not current_url.startswith("https://www.instagram.com/12storeez/"): # СЮДА СТАВИМ ССЫЛКУ НА ПРОФИЛЬ, КОТОРЫЙ ПАРСИМ, МЕНЯТЬ ТУТ И В ДВУХ МЕСТАХ НИЖЕ ⏬
        pag.click(23, 62, button='left')
        time.sleep(0.5)
        pag.click(1914, 1029, 4, 1, button='left')

    # 🔹 Первый пост
    pag.moveTo(790, 550)
    time.sleep(0.2)
    pag.click(790, 550, button='right')
    time.sleep(0.2)
    pag.click(926, 729, button='left')
    time.sleep(0.2)
    pag.hotkey('ctrl', 'c')
    time.sleep(0.2)
    all_links.append(pyperclip.paste().strip())


    # 🔎 Проверка текущего URL
    pag.click(301, 63, button='right')
    time.sleep(0.2)
    pag.click(380, 256, button='left')
    time.sleep(0.2)
    current_url = pyperclip.paste().strip()

    if not current_url.startswith("https://www.instagram.com/12storeez/"): # СЮДА
        pag.click(23, 62, button='left')
        time.sleep(0.5)
        pag.click(1914, 1029, 4, 1, button='left')

    # 🔹 Второй пост
    pag.moveTo(1123, 600)
    time.sleep(0.2)
    pag.click(1123, 600, button='right')
    time.sleep(0.2)
    pag.click(1252, 772, button='left')
    time.sleep(0.2)
    pag.hotkey('ctrl', 'c')
    time.sleep(0.2)
    all_links.append(pyperclip.paste().strip())


    # 🔎 Проверка текущего URL
    pag.click(301, 63, button='right')
    time.sleep(0.2)
    pag.click(380, 256, button='left')
    time.sleep(0.2)
    current_url = pyperclip.paste().strip()

    if not current_url.startswith("https://www.instagram.com/12storeez/"): # СЮДА
        pag.click(23, 62, button='left')
        time.sleep(0.5)
        pag.click(1914, 1029, 4, 1, button='left')

    # 🔹 Третий пост
    pag.moveTo(1445, 600)
    time.sleep(0.2)
    pag.click(1445, 600, button='right')
    time.sleep(0.2)
    pag.click(1543, 774, button='left')
    time.sleep(0.2)
    pag.hotkey('ctrl', 'c')
    time.sleep(0.2)
    all_links.append(pyperclip.paste().strip())

    # 🔄 Скроллим вниз
    pag.scroll(-500, 0, 0)
    time.sleep(0.4)

    # 💾 Сохраняем в Excel
    df = pd.DataFrame(all_links, columns=["Post Links"])
    df.to_excel("instagram_collected_links.xlsx", index=False)
    print(f"\n📄 Сохранено {len(all_links)} ссылок в файл 'instagram_collected_links.xlsx'")

