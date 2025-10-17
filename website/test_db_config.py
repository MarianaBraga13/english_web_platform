from config import load_encrypted_config  # sem 'website.'
from pathlib import Path

config_file = Path(__file__).parent / 'database.ini'
db_config = load_encrypted_config(config_file)

print("Configurações carregadas do database.ini:")
for key, value in db_config['postgresql'].items():
    print(f"{key}: {value}")
