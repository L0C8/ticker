
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


def _load_users(accounts_file: Path | str) -> dict:
    try:
        with open(accounts_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    return data.get("users", {})


def _save_users(accounts_file: Path | str, users: dict) -> None:
    with open(accounts_file, "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, indent=4)


def create_account(username: str, pw1: str, pw2: str, accounts_file: Path | str) -> tuple[bool, str]:
    if not username or not pw1:
        return False, "Username and password required"
    if pw1 != pw2:
        return False, "Passwords do not match"

    users = _load_users(accounts_file)
    for enc_user in users.keys():
        try:
            dec_user = AESCipherPass.decrypt(enc_user, "default")
        except Exception:
            continue
        if dec_user == username:
            return False, "Username already exists"

    enc_user = AESCipherPass.encrypt(username, "default")
    ciphered_pw = AESCipherPass.encrypt(pw1, "default")
    hashed_pw = hash_text(ciphered_pw)
    enc_pw = AESCipherPass.encrypt(hashed_pw, pw1)
    users[enc_user] = {"password": enc_pw, "finnhub": ""}
    _save_users(accounts_file, users)
    return True, "Account created"


def login_account(username: str, password: str, accounts_file: Path | str) -> tuple[bool, str | None]:
    if not username or not password:
        return False, None

    users = _load_users(accounts_file)
    ciphered_input = AESCipherPass.encrypt(password, "default")
    hashed_input = hash_text(ciphered_input)

    for enc_user, info in users.items():
        try:
            dec_user = AESCipherPass.decrypt(enc_user, "default")
        except Exception:
            continue
        if dec_user == username:
            stored_enc = info.get("password", "")
            try:
                stored_hash = AESCipherPass.decrypt(stored_enc, password)
            except Exception:
                break
            if stored_hash == hashed_input:
                return True, enc_user
            break

    return False, None
