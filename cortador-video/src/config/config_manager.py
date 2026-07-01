"""Gerenciador de configurações do usuário."""

import os
import json
from typing import Dict, Any
from .settings import Settings


class ConfigManager:
    """Gerencia o arquivo de configuração do usuário."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.config_file = os.path.join(
            settings.CONFIG_DIR,
            settings.DEFAULT_CONFIG_FILE
        )
        self.config = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Arquivo de configuração corrompido. Criando novo.")
                return {}
        return {}
    
    def save(self) -> None:
        """Salva configurações no arquivo."""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar configurações: {e}")
    
    def get_last_directory(self) -> str:
        """Retorna o último diretório usado."""
        return self.config.get('last_output_directory', '')
    
    def set_last_directory(self, directory: str) -> None:
        """Define o último diretório usado."""
        self.config['last_output_directory'] = directory