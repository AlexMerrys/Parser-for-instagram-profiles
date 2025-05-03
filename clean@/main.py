import pandas as pd

# Загружаем исходный файл (укажи нужное имя)
df = pd.read_excel("mentions_raw.xlsx")  # или .csv

# Колонка, где хранятся @упоминания
column = "Mentions"

# Список для очищенных значений
clean_mentions = []

for value in df[column]:
    if pd.isna(value):
        continue
    # Разделяем по запятой, убираем пустые и пробелы
    parts = [mention.strip() for mention in str(value).split(",") if mention.strip()]
    clean_mentions.extend(parts)

# Создаём DataFrame
df_clean = pd.DataFrame(clean_mentions, columns=["Cleaned Mentions"])

# Сохраняем в Excel
df_clean.to_excel("mentions_cleaned.xlsx", index=False)

print("✅ Упоминания сохранены в 'mentions_cleaned.xlsx'")
