from cryptography.fernet import Fernet
import configparser
from pathlib import Path

def encrypt_config(filename, key):
    cipher_suite = Fernet(key)
    config = configparser.ConfigParser()
    config.read(filename, encoding='utf-8')

    # Verifica se já está criptografado
    first_value = list(config[config.sections()[0]].values())[0]
    if first_value.startswith("gAAAAA"):
        print("⚠️ O arquivo já está criptografado.")
        return

    for section in config.sections():
        for option in config[section]:
            encrypted_value = cipher_suite.encrypt(config[section][option].encode())
            config[section][option] = encrypted_value.decode()

    with open(filename, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

# Caminho do arquivo .ini
config_file = Path(__file__).parent / 'database.ini'

# Gera chave e criptografa
key = Fernet.generate_key()
encrypt_config(config_file, key)

# Salva a chave
with open('encryption_key.txt', 'wb') as key_file:
    key_file.write(key)

print("✅ Configurações criptografadas com sucesso.")