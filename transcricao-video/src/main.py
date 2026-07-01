#!/usr/bin/env python
"""Programa de transcrição de vídeos usando Whisper."""

import sys
import os
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent))

from core.transcriber import VideoTranscriber
from ui.console_ui import ConsoleUI
from config.settings import Settings
from utils.logger import setup_logger


class TranscriptionApp:
    """Aplicação principal de transcrição."""
    
    def __init__(self):
        self.settings = Settings()
        self.logger = setup_logger('transcricao', self.settings.LOG_DIR)
        self.ui = ConsoleUI()
        self.transcriber = VideoTranscriber(self.settings, self.logger)
        self.running = True
    
    def run(self):
        """Executa a aplicação."""
        try:
            self.ui.show_header()
            
            while self.running:
                try:
                    self.process_video()
                except KeyboardInterrupt:
                    print("\nOperação cancelada pelo usuário.")
                    break
                except Exception as e:
                    self.logger.error(f"Erro: {e}")
                    self.ui.show_error(str(e))
                    continue
                
                if not self.ui.prompt_continue():
                    self.running = False
            
            self.ui.show_footer()
            
        except Exception as e:
            self.logger.critical(f"Erro fatal: {e}")
            self.ui.show_error(f"Erro fatal: {e}")
            sys.exit(1)
    
    def process_video(self):
        """Processa um vídeo para transcrição."""
        # 1. Solicita vídeo
        video_path = self.ui.prompt_input_video()
        if not video_path:
            return
        
        # 2. Verifica se o vídeo existe
        if not os.path.exists(video_path):
            self.ui.show_error("Arquivo não encontrado!")
            return
        
        # 3. Solicita opções de transcrição
        model_size = self.ui.prompt_model_size()
        language = self.ui.prompt_language()
        
        # 4. Pergunta onde salvar
        output_path = self.ui.prompt_output_path(video_path)
        if not output_path:
            return
        
        # 5. Processa a transcrição
        self.ui.show_processing()
        result = self.transcriber.transcribe(
            video_path=video_path,
            output_path=output_path,
            model_size=model_size,
            language=language
        )
        
        # 6. Mostra resultado
        if result:
            self.ui.show_success(output_path)
            self.ui.show_preview(result)
        else:
            self.ui.show_error("Falha na transcrição.")


def main():
    """Função principal."""
    app = TranscriptionApp()
    app.run()


if __name__ == "__main__":
    main()