import os
import pandas as pd
import requests
from datetime import datetime

def send_parse_report(csv_file, bot_token, chat_id, log_file="last_count.txt"):
    """
    Отправляет в Telegram отчёт о количестве строк в CSV и разнице с прошлым запуском.

    :param csv_file: путь к CSV файлу
    :param bot_token: токен бота Telegram от @BotFather
    :param chat_id: твой chat_id в Telegram
    :param log_file: путь к файлу, где хранится прошлое количество строк
    """
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Файл {csv_file} не найден")

    # Загружаем таблицу
    df = pd.read_csv(csv_file)
    current_count = len(df)

    # Читаем прошлое значение
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            last_count = int(f.read().strip() or 0)
    else:
        last_count = 0

    diff = current_count - last_count

    # Формируем сообщение
    message = (
        f"📊 *Отчёт по парсингу*\n\n"
        f"🗂 Всего строк: *{current_count:,}*\n"
        f"📈 Новых с прошлого раза: *{diff:,}*\n"
        f"🕒 Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"📄 Файл: `{os.path.basename(csv_file)}`"
    )

    # Отправляем в Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    r = requests.post(url, data=data)
    if r.status_code != 200:
        raise RuntimeError(f"Ошибка отправки в Telegram: {r.text}")

    # Сохраняем новое значение
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(str(current_count))
