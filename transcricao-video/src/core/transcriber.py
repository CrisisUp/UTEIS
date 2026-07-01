"""Núcleo da transcrição de vídeos."""

import os
import tempfile
from typing import Optional, Dict, Any
import whisper
from moviepy import VideoFileClip
from config.settings import Settings
from ui.colors import Colors


class VideoTranscriber:
    """Transcreve áudio de vídeos usando Whisper."""
    
    def __init__(self, settings: Settings, logger):
        self.settings = settings
        self.logger = logger
        self.model = None
        self.colors = Colors()
    
    def _load_model(self, model_size: str = "base"):
        """Carrega o modelo Whisper."""
        if self.model is None:
            self.logger.info(f"Carregando modelo Whisper '{model_size}'...")
            print(f"{self.colors.YELLOW}📥 Baixando modelo Whisper '{model_size}'... Isso pode demorar!{self.colors.RESET}")
            self.model = whisper.load_model(model_size)
            self.logger.info("Modelo carregado com sucesso!")
            print(f"{self.colors.GREEN}✅ Modelo carregado com sucesso!{self.colors.RESET}")
        return self.model
    
    def _extract_audio(self, video_path: str) -> str:
        """Extrai o áudio do vídeo para um arquivo temporário."""
        self.logger.info(f"Extraindo áudio de: {video_path}")
        print(f"{self.colors.CYAN}🎵 Extraindo áudio do vídeo...{self.colors.RESET}")
        
        # Cria arquivo temporário para o áudio
        temp_audio = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        try:
            # Extrai o áudio
            video = VideoFileClip(video_path)
            audio = video.audio
            
            if audio is None:
                raise ValueError("O vídeo não contém áudio!")
            
            # Salva o áudio como WAV - REMOVIDO O PARÂMETRO verbose
            audio.write_audiofile(
                temp_audio_path,
                codec='pcm_s16le',
                fps=16000,
                nbytes=2,
                logger=None  # verbose foi removido no MoviePy 2.2.1
            )
            
            video.close()
            audio.close()
            
            self.logger.info(f"Áudio extraído para: {temp_audio_path}")
            print(f"{self.colors.GREEN}✅ Áudio extraído com sucesso!{self.colors.RESET}")
            return temp_audio_path
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair áudio: {e}")
            raise
    
    def transcribe(
        self,
        video_path: str,
        output_path: str = None,
        model_size: str = "base",
        language: str = None
    ) -> Optional[str]:
        """
        Transcreve o áudio de um vídeo.
        
        Args:
            video_path: Caminho do vídeo
            output_path: Caminho para salvar a transcrição (opcional)
            model_size: Tamanho do modelo ('tiny', 'base', 'small', 'medium', 'large')
            language: Código do idioma (ex: 'pt', 'en', 'es')
        
        Returns:
            str: Texto transcrito ou None em caso de erro
        """
        temp_audio_path = None
        
        try:
            # 1. Carrega o modelo
            model = self._load_model(model_size)
            
            # 2. Extrai o áudio
            temp_audio_path = self._extract_audio(video_path)
            
            # 3. Transcreve
            self.logger.info("Iniciando transcrição...")
            print(f"{self.colors.CYAN}🤖 Transcrevendo áudio... Isso pode levar alguns minutos...{self.colors.RESET}")
            
            options = {}
            if language:
                options['language'] = language
            
            result = model.transcribe(
                temp_audio_path,
                **options
            )
            
            transcript_text = result['text']
            self.logger.info(f"Transcrição concluída! ({len(transcript_text)} caracteres)")
            print(f"{self.colors.GREEN}✅ Transcrição concluída!{self.colors.RESET}")
            
            # 4. Salva se um caminho foi fornecido
            if output_path:
                self._save_transcript(transcript_text, output_path)
                self.logger.info(f"Transcrição salva em: {output_path}")
            
            return transcript_text
            
        except Exception as e:
            self.logger.error(f"Erro na transcrição: {e}")
            return None
            
        finally:
            # Limpa arquivo temporário
            if temp_audio_path and os.path.exists(temp_audio_path):
                try:
                    os.unlink(temp_audio_path)
                    self.logger.info("Arquivo temporário removido")
                except:
                    pass
    
    def _save_transcript(self, text: str, output_path: str):
        """Salva a transcrição em um arquivo."""
        # Garante que o diretório existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Salva o arquivo principal
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Também salva uma versão com timestamp
        base, ext = os.path.splitext(output_path)
        timestamp_path = f"{base}_{self._get_timestamp()}{ext}"
        with open(timestamp_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"{self.colors.GREEN}📄 Arquivos salvos:{self.colors.RESET}")
        print(f"   - {output_path}")
        print(f"   - {timestamp_path}")
    
    def _get_timestamp(self) -> str:
        """Retorna timestamp para nome de arquivo."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")