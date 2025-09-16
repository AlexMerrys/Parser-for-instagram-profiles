# Отчиста ссылок от лишнего. в "instagram_links_raw" до, а в "instagram_links_cleaned" после

import pandas as pd

# Загрузка исходного файла
df = pd.read_excel("instagram_links_raw.xlsx")  # или .csv

# Колонка, где лежат ссылки
column = "Post Links"

# Новый список, куда положим каждую ссылку отдельно
clean_links = []

# Проходим по каждой строке
for value in df[column]:
    if pd.isna(value):
        continue
    # Разделяем по запятой и пробелу, убираем лишнее
    parts = [link.strip() for link in str(value).split(",")]
    clean_links.extend(parts)

# Создаём DataFrame с одной ссылкой на строку
df_clean = pd.DataFrame(clean_links, columns=["Instagram Links"])

# Сохраняем результат
df_clean.to_excel("instagram_links_cleaned.xlsx", index=False)
print("✅ Готово: сохранено в 'instagram_links_cleaned.xlsx'")

