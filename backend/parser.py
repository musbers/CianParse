import requests
import json
import pandas as pd
import os
from config import TABLES_XLSX, TABLES_CSV, MEGA_TABLE, BASE_DIR
from report_sender import send_parse_report


BOT_TOKEN = "8314940310:AAGLIxgVV0BPru65hD4ZrIDTpLeOjMnGgeI"
CHAT_ID = "7366647016"


def download_file(url, filepath):
    res = requests.get(url)
    res.raise_for_status()
    filepath.write_bytes(res.content)

def run_parser():
    with open(BASE_DIR / "cities.json", "r", encoding="utf-8") as file:
        cities = json.load(file)

    # 1. Скачивание
    for city in cities:
        id = city["id"]
        name = city["name"]
        download_url = f"https://krasnodar.cian.ru/export/xls/offers/?cats%5B0%5D=commercialLandSale&deal_type=sale&engine_version=2&offer_type=offices&region={id}"
        file_path = TABLES_XLSX / f"{name}.xlsx"
        try:
            download_file(download_url, file_path)
            print("Скачано:", name)
        except Exception as e:
            print(f"Ошибка при скачивании {name}: {e}")

    # 2. Конвертация
    for file in os.listdir(TABLES_XLSX):
        df = pd.read_excel(TABLES_XLSX / file)
        if not df.empty:
            csv_file = TABLES_CSV / file.replace(".xlsx", ".csv")
            df.to_csv(csv_file, index=False, encoding="utf-8")
        else:
            print("Пустой файл:", file)

    # 3. Объединение
    dfs = []
    for file in os.listdir(TABLES_CSV):
        dfs.append(pd.read_csv(TABLES_CSV / file))
    mega_df = pd.concat(dfs, ignore_index=True)
    mega_df.to_csv(MEGA_TABLE, index=False, encoding="utf-8")
    print("Обновлён mega_table.csv")
    try:
        send_parse_report(BASE_DIR/'data'/'mega_table.csv', BOT_TOKEN, CHAT_ID)
    except: {}

if __name__ == "__main__":
    run_parser()
