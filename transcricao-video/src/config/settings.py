"""Configurações da aplicação."""

from dataclasses import dataclass, field
from typing import List
import os


@dataclass
class Settings:
    """Configurações da aplicação."""
    
    CONFIG_DIR: str = "data/config"
    LOG_DIR: str = "data/logs"
    
    MODEL_SIZE: str = "base"
    LANGUAGE: str = None
    
    SUPPORTED_FORMATS: List[str] = field(default_factory=lambda: [
        '.mp4', '.avi', '.mov', '.mkv',
        '.webm', '.flv', '.wmv', '.mpeg', '.mpg'
    ])
    
    def __post_init__(self):
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)