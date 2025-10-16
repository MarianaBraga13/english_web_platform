from cryptography.fernet import Fernet
import configparser
from pathlib import Path

def load_encrypted_config(file_path):
    # Lê a chave salva
    key_path = Path(__file__).parent / 'encryption_key.txt'
    with open(key_path, 'rb') as key_file:
        key = key_file.read().strip()

    cipher_suite = Fernet(key)
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')

    decrypted = {}
    for section in config.sections():
        decrypted[section] = {}
        for k, v in config[section].items():
            try:
                decrypted_value = cipher_suite.decrypt(v.encode()).decode()
                decrypted[section][k] = decrypted_value
            except Exception:
                decrypted[section][k] = v  # se não estiver criptografado, mantém o valor

    return decrypted