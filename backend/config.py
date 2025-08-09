from pathlib import Path

# Пароль для входа на сайт
PASSWORD = "superpass"  # поменяй на свой

# Пути
BASE_DIR = Path(__file__).resolve().parent.parent
TABLES_XLSX = BASE_DIR / "data" / "tables_xlsx"
TABLES_CSV = BASE_DIR / "data" / "tables_csv"
MEGA_TABLE = BASE_DIR / "data" / "mega_table.csv"

# Убедимся, что папки созданы
TABLES_XLSX.mkdir(parents=True, exist_ok=True)
TABLES_CSV.mkdir(parents=True, exist_ok=True)
