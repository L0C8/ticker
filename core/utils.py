
from pathlib import Path
import json
from core.cipher import AESCipherPass, hash_text

def bootcheck():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    accounts_file = data_dir / "accounts.json"
    
    if not accounts_file.exists():
        default_user = "admin"
        default_pass = "admin"
        enc_user = AESCipherPass.encrypt(default_user, "default")
        ciphered_pw = AESCipherPass.encrypt(default_pass, "default")
        hashed = hash_text(ciphered_pw)
        enc_pass_hash = AESCipherPass.encrypt(hashed, default_pass)
        data = {"users": {enc_user: {"password": enc_pass_hash, "finnhub": ""}}}
        with accounts_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    print("Bootcheck passed.")
