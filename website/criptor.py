from cryptography.fernet import Fernet
import configparser
from pathlib import Path

def encrypt_config(filename, key):
    # Inicializar o objeto Fernet com a chave fornecida
    cipher_suite = Fernet(key)
    
    # Carregar o arquivo de configuração
    config = configparser.ConfigParser()
    config.read(filename, encoding='utf-8')

    # Iterar sobre todas as seções e chaves do arquivo de configuração
    for section in config.sections():
        for key in config[section]:
            # Criptografar o valor atual e atualizar no arquivo
            encrypted_value = cipher_suite.encrypt(config[section][key].encode())
            config[section][key] = encrypted_value.decode()

    # Escrever as configurações de volta no arquivo
    with open(filename, 'w') as configfile:
        config.write(configfile)

# Caminho do arquivo de configuração
config_file = Path(__file__).parent / 'database.ini'

# Gerar uma chave de criptografia e criptografar o arquivo de configuração
key = Fernet.generate_key()
encrypt_config(config_file, key)

# Salvar a chave de criptografia em um arquivo
with open('encryption_key.txt', 'wb') as key_file:
    key_file.write(key)

print("Configurações criptografadas com sucesso.")