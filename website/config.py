from cryptography.fernet import Fernet
import configparser
from pathlib import Path

# Função para descriptografar os dados do arquivo de configuração
def decrypt_config(filename, key):
    # Inicializar o objeto Fernet com a chave fornecida
    cipher_suite = Fernet(key)
    
    # Carregar o arquivo de configuração
    config = configparser.ConfigParser()
    config.read(filename, encoding='utf-8')

    # Iterar sobre todas as seções e chaves do arquivo de configuração
    for section in config.sections():
        for key in config[section]:
            try:
                # Tentar decifrar o valor atual
                decrypted_value = cipher_suite.decrypt(config[section][key].encode()).decode()
                # Atualizar o valor decifrado no arquivo de configuração
                config[section][key] = decrypted_value
            except:
                # Se a descriptografia falhar, manter o valor original
                pass

    return config

# Caminho do arquivo de configuração
config_file = Path(__file__).parent / 'database.ini'

# Carregar a chave de criptografia do arquivo
with open('encryption_key.txt', 'rb') as key_file:
    key = key_file.read()

# Descriptografar o arquivo de configuração
config = decrypt_config(config_file, key)

# Configurações do banco de dados PostgreSQL
db_config = {
    'hostname': config['postgresql']['hostname'],
    'port': config['postgresql'].getint('port'),
    'database': config['postgresql']['database'],
    'username': config['postgresql']['username'],
    'password': config['postgresql']['password']
}

# Configurações do servidor SSH
ssh_config = {
    'jumpserver': config['ssh']['jumpserver'],
    'ssh_user': config['ssh']['ssh_user'],
    'ssh_key_path': config['ssh']['ssh_key_path']
}