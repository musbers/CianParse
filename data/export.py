import pandas as pd

# Читаем CSV
df = pd.read_csv("mega_table.csv")

# Сохраняем в XLSX
df.to_excel("output.xlsx", index=False)
