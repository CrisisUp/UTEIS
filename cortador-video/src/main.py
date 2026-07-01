#!/usr/bin/env python
"""Ponto de entrada principal do programa."""

import sys
import os
from pathlib import Path

# Adiciona src ao path para importações
sys.path.insert(0, str(Path(__file__).parent))

# Importações da aplicação
from ui.colors import Colors          # ← Importação adicionada
from core.video_cutter import VideoCutter
from ui.console_ui import ConsoleUI
from config.config_manager import ConfigManager
from config.settings import Settings
from utils.logger import setup_logger
from exceptions.video_exceptions import VideoCutterError


class VideoCutterApp:
    """Classe principal da aplicação."""
    
    def __init__(self):
        """Inicializa a aplicação."""
        self.settings = Settings()
        self.logger = setup_logger('video_cutter', self.settings.LOG_DIR)
        self.config_manager = ConfigManager(self.settings)
        self.ui = ConsoleUI()
        self.cutter = VideoCutter(self.settings, self.logger)
        self.running = True
        self.colors = Colors()  # ← Adicionado para uso no main
    
    def run(self):
        """Executa a aplicação."""
        try:
            self.ui.show_header()
            
            while self.running:
                try:
                    self.process_video_flow()
                except KeyboardInterrupt:
                    print(f"\n{self.colors.YELLOW}Operação cancelada pelo usuário.{self.colors.RESET}")
                    break
                except Exception as e:
                    self.logger.error(f"Erro: {e}")
                    self.ui.show_error(str(e))
                    continue
                
                # Pergunta se quer continuar
                if not self.ui.prompt_continue():
                    self.running = False
            
            self.ui.show_footer()
            
        except Exception as e:
            self.logger.critical(f"Erro fatal: {e}")
            self.ui.show_error(f"Erro fatal: {e}")
            sys.exit(1)
    
    def process_video_flow(self):
        """Fluxo principal de processamento de vídeo."""
        # 1. Solicita vídeo de entrada
        input_path = self.ui.prompt_input_video()
        if not input_path:
            return
        
        # 2. Obtém duração
        duration = self.cutter.get_duration(input_path)
        if duration is None:
            self.ui.show_error("Não foi possível obter a duração do vídeo.")
            return
        
        # 3. Mostra duração
        self.ui.show_duration(duration)
        
        # 4. Solicita tempos de corte
        start_time, end_time = self.ui.prompt_cut_times(duration)
        if start_time is None or end_time is None:
            return
        
        # 5. Gera caminho de saída sugerido
        suggested_output = self.cutter.suggest_output_path(
            input_path, 
            self.config_manager.get_last_directory()
        )
        
        # 6. Solicita caminho de saída
        output_path = self.ui.prompt_output_path(suggested_output)
        if not output_path:
            return
        
        # 7. Salva configuração
        self.config_manager.set_last_directory(os.path.dirname(output_path))
        self.config_manager.save()
        
        # 8. Processa o corte
        self.ui.show_processing()
        success = self.cutter.cut_video(input_path, output_path, start_time, end_time)
        
        # 9. Mostra resultado
        if success:
            self.ui.show_success(output_path)
        else:
            self.ui.show_error("Falha ao cortar o vídeo.")


def check_ffmpeg():
    """Verifica se o FFmpeg está instalado."""
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, 
                      check=True)
        return True
    except:
        return False


def main():
    """Função principal."""
    # Cria instância para usar cores
    colors = Colors()
    
    # Verifica FFmpeg
    if not check_ffmpeg():
        print(f"{colors.RED}❌ FFmpeg não encontrado!{colors.RESET}")
        print("   Instale o FFmpeg: https://ffmpeg.org/download.html")
        sys.exit(1)
    
    # Executa aplicação
    app = VideoCutterApp()
    app.run()


if __name__ == "__main__":
    main()