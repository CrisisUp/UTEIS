"""Núcleo do cortador de vídeo."""

import os
from typing import Optional, Tuple
from moviepy import VideoFileClip
from config.settings import Settings
from utils.time_utils import TimeUtils
from utils.file_utils import FileUtils


class VideoCutter:
    """Classe principal para corte de vídeos."""
    
    def __init__(self, settings: Settings, logger):
        self.settings = settings
        self.logger = logger
        self.time_utils = TimeUtils()
        self.file_utils = FileUtils()
    
    def get_duration(self, video_path: str) -> Optional[float]:
        """Obtém a duração do vídeo em segundos."""
        clip = None
        try:
            self.logger.info(f"Obtendo duração do vídeo: {video_path}")
            clip = VideoFileClip(video_path)
            duration = clip.duration
            self.logger.info(f"Duração: {duration:.2f} segundos")
            return duration
        except Exception as e:
            self.logger.error(f"Erro ao obter duração: {e}")
            return None
        finally:
            if clip:
                clip.close()
    
    def cut_video(
        self,
        input_path: str,
        output_path: str,
        start_time: float,
        end_time: float
    ) -> bool:
        """Corta um vídeo no intervalo especificado."""
        clip = None
        try:
            # Carrega vídeo
            self.logger.info(f"Carregando vídeo: {input_path}")
            clip = VideoFileClip(input_path)
            
            # Valida tempos
            if not self._validate_times(start_time, end_time, clip.duration):
                return False
            
            # Corta
            self.logger.info(f"Cortando de {start_time}s a {end_time}s")
            cut_clip = clip[start_time:end_time]
            
            # Salva - REMOVIDO O PARÂMETRO verbose
            self.logger.info(f"Salvando em: {output_path}")
            cut_clip.write_videofile(
                output_path,
                codec=self.settings.VIDEO_CODEC,
                audio_codec=self.settings.AUDIO_CODEC,
                logger=None  # verbose foi removido
            )
            
            self.logger.info("Corte concluído com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao cortar vídeo: {e}")
            return False
        finally:
            if clip:
                clip.close()
    
    def _validate_times(self, start: float, end: float, duration: float) -> bool:
        """Valida os tempos de corte."""
        if start < 0 or end > duration or start >= end:
            self.logger.error(f"Tempos inválidos: {start}s - {end}s (duração: {duration}s)")
            return False
        return True
    
    def suggest_output_path(self, input_path: str, last_directory: str = "") -> str:
        """Gera um caminho de saída sugerido."""
        base_name, ext = os.path.splitext(os.path.basename(input_path))
        ext = ext.lstrip('.') or 'mp4'
        filename = f"{base_name}_cortado.{ext}"
        
        if last_directory:
            return os.path.join(last_directory, filename)
        else:
            return os.path.join(os.path.dirname(input_path), filename)