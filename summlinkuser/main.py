import pandas as pd

# Загружаем таблицу с @usernames
df = pd.read_excel("usernames_raw.xlsx")  # Заменить на имя твоего файла
column = "Mentions"  # Название колонки с @юзернеймами

# Удаляем @ и добавляем к ссылке
df["Instagram Link"] = "https://www.instagram.com/" + df[column].str.replace("@", "").str.strip()

# Сохраняем результат
df.to_excel("instagram_links_converted.xlsx", index=False)

print("✅ Ссылки сохранены в 'instagram_links_converted.xlsx'")
