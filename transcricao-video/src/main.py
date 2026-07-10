#!/usr/bin/env python
"""Programa de transcrição de vídeos e áudios usando Whisper."""

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
        
        # Verifica FFmpeg na inicialização
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        """Verifica se o FFmpeg está instalado."""
        import subprocess
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            self.logger.info("FFmpeg encontrado")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning("FFmpeg não encontrado")
            print("\n⚠️  FFmpeg não encontrado no sistema!")
            print("   O programa pode não funcionar corretamente com alguns formatos.")
            print("   Instale o FFmpeg:")
            print("     - macOS: brew install ffmpeg")
            print("     - Ubuntu: sudo apt install ffmpeg")
            print("     - Windows: Baixe de https://ffmpeg.org/\n")
            return False
    
    def run(self):
        """Executa a aplicação."""
        try:
            self.ui.show_header()
            
            while self.running:
                try:
                    self.process_video()
                except KeyboardInterrupt:
                    print("\n⏹️  Operação cancelada pelo usuário.")
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
        """Processa um vídeo ou áudio para transcrição."""
        # 1. Solicita arquivo
        video_path = self.ui.prompt_input_video()
        if not video_path:
            return
        
        # Remove aspas se houver
        video_path = video_path.strip('"\'')
        
        # 2. Verifica se o arquivo existe
        if not os.path.exists(video_path):
            self.ui.show_error("Arquivo não encontrado!")
            return
        
        # 3. Mostra informações do arquivo
        self._show_file_info(video_path)
        
        # 4. Solicita opções de transcrição
        model_size = self.ui.prompt_model_size()
        language = self.ui.prompt_language()
        
        # Pergunta se quer traduzir para inglês
        translate = self.ui.prompt_translate()
        
        # 5. Pergunta onde salvar
        output_path = self.ui.prompt_output_path(video_path)
        if not output_path:
            return
        
        # Verifica se o arquivo de saída já existe
        if os.path.exists(output_path):
            if not self.ui.prompt_overwrite(output_path):
                return
        
        # 6. Processa a transcrição
        self.ui.show_processing()
        
        # Determina a tarefa (transcrever ou traduzir)
        task = "translate" if translate else "transcribe"
        
        result = self.transcriber.transcribe(
            video_path=video_path,
            output_path=output_path,
            model_size=model_size,
            language=language,
            task=task
        )
        
        # 7. Mostra resultado
        if result:
            self.ui.show_success(output_path)
            self.ui.show_preview(result)
            
            # Pergunta se quer salvar em formatos adicionais
            if self.ui.prompt_extra_formats():
                self._save_extra_formats(result, output_path)
        else:
            self.ui.show_error("Falha na transcrição.")
    
    def _show_file_info(self, file_path: str):
        """Mostra informações do arquivo."""
        import os
        from datetime import datetime
        
        size = os.path.getsize(file_path)
        size_mb = size / (1024 * 1024)
        
        # Determina o tipo de arquivo
        ext = os.path.splitext(file_path)[1].lower()
        audio_exts = ['.mp3', '.m4a', '.aac', '.flac', '.ogg', '.wav', '.wma']
        video_exts = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm', '.mpeg']
        
        if ext in audio_exts:
            file_type = "Áudio"
        elif ext in video_exts:
            file_type = "Vídeo"
        else:
            file_type = "Desconhecido"
        
        print(f"\n📁 Arquivo: {os.path.basename(file_path)}")
        print(f"   Tipo: {file_type} ({ext})")
        print(f"   Tamanho: {size_mb:.2f} MB")
        print(f"   Modificado: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y %H:%M')}")
    
    def _save_extra_formats(self, text: str, output_path: str):
        """Salva a transcrição em formatos adicionais."""
        base_path = os.path.splitext(output_path)[0]
        
        # Salva como SRT (legendas)
        srt_path = f"{base_path}.srt"
        self._save_as_srt(text, srt_path)
        print(f"   ✅ Legendas SRT: {srt_path}")
        
        # Salva como JSON com metadados
        json_path = f"{base_path}.json"
        self._save_as_json(text, json_path, output_path)
        print(f"   ✅ JSON: {json_path}")
    
    def _save_as_srt(self, text: str, output_path: str):
        """Salva como arquivo SRT (simplificado)."""
        # Versão simplificada - apenas coloca o texto como uma legenda
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("1\n")
            f.write("00:00:00,000 --> 00:59:59,999\n")
            f.write(text + "\n\n")
    
    def _save_as_json(self, text: str, output_path: str, original_path: str):
        """Salva como JSON com metadados."""
        import json
        from datetime import datetime
        
        data = {
            "texto": text,
            "caracteres": len(text),
            "palavras": len(text.split()),
            "arquivo_original": os.path.basename(original_path),
            "data_transcricao": datetime.now().isoformat(),
            "modelo": "Whisper"
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    """Função principal."""
    try:
        app = TranscriptionApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Programa encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()