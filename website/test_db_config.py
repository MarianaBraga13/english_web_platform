from pathlib import Path
from website.config import load_encrypted_config

# Caminho para o arquivo database.ini
config_file = Path(__file__).parent / 'website' / 'database.ini'

# Carrega e descriptografa as configurações
db_config = load_encrypted_config(config_file)

# Exibe as configurações descriptografadas
print("Configurações carregadas do database.ini:")
for key, value in db_config['postgresql'].items():
    print(f"{key}: {value}")