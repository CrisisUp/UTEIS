"""Configuração de logging."""

import logging
import os
from datetime import datetime


def setup_logger(name: str, log_dir: str) -> logging.Logger:
    """Configura o logger da aplicação."""
    # Cria o logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Cria o diretório de logs
    os.makedirs(log_dir, exist_ok=True)
    
    # Nome do arquivo de log com data
    log_file = os.path.join(log_dir, f"{name}_{datetime.now():%Y%m%d}.log")
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adiciona handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger