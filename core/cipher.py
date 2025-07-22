from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib, base64, os

class AESCipherPass:
    backend = default_backend()

    @staticmethod
    def set_key(password):
        sha1 = hashlib.sha1(password.encode())
        return sha1.digest()[:16]

    @staticmethod
    def encrypt(plaintext, password):
        key = AESCipherPass.set_key(password)
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=AESCipherPass.backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode()

    @staticmethod
    def decrypt(ciphertext, password):
        try:
            key = AESCipherPass.set_key(password)
            encrypted_data = base64.b64decode(ciphertext)
            cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=AESCipherPass.backend)
            decryptor = cipher.decryptor()

            decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

            return decrypted_data.decode()
        except Exception as e:
            return f"Error decrypting: {e}"

def hash_text(text, method='sha256'):
    h = getattr(hashlib, method)()
    h.update(text.encode('utf-8'))
    return h.hexdigest()