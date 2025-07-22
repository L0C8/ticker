
from pathlib import Path
import configparser

def bootcheck():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    accounts_file = data_dir / "accounts.ini"
    if not accounts_file.exists():
        config = configparser.ConfigParser()
        config["users"] = {"admin": "admin"}
        with accounts_file.open("w", encoding="utf-8") as f:
            config.write(f)

    print("Bootcheck passed.")