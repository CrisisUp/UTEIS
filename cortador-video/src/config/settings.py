"""Configurações da aplicação."""

from dataclasses import dataclass, field
from typing import List
import os


@dataclass
class Settings:
    """Configurações da aplicação."""
    
    # Diretórios
    CONFIG_DIR: str = "data/config"
    LOG_DIR: str = "data/logs"
    
    # Codecs
    VIDEO_CODEC: str = "libx264"
    AUDIO_CODEC: str = "aac"
    
    # Formatos suportados - USANDO default_factory PARA LISTAS
    SUPPORTED_FORMATS: List[str] = field(default_factory=lambda: [
        '.mp4', '.avi', '.mov', '.mkv',
        '.webm', '.flv', '.wmv', '.mpeg', '.mpg'
    ])
    
    # Limites
    MAX_FILE_SIZE_MB: int = 1024
    DEFAULT_CONFIG_FILE: str = "video_cutter_config.json"
    
    def __post_init__(self):
        """Cria diretórios necessários após inicialização."""
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)