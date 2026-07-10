"""Núcleo da transcrição de vídeos e áudios."""

import os
import tempfile
import subprocess
from typing import Optional, Dict, Any
import whisper
from moviepy import VideoFileClip, AudioFileClip
from config.settings import Settings
from ui.colors import Colors


class VideoTranscriber:
    """Transcreve áudio de vídeos ou arquivos de áudio usando Whisper."""
    
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
    
    def _is_audio_file(self, file_path: str) -> bool:
        """Verifica se o arquivo é um arquivo de áudio."""
        audio_extensions = ['.mp3', '.m4a', '.aac', '.flac', '.ogg', '.wav', '.wma', '.aiff']
        ext = os.path.splitext(file_path)[1].lower()
        return ext in audio_extensions
    
    def _is_video_file(self, file_path: str) -> bool:
        """Verifica se o arquivo é um arquivo de vídeo."""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm', '.mpeg', '.mpg']
        ext = os.path.splitext(file_path)[1].lower()
        return ext in video_extensions
    
    def _extract_audio(self, video_path: str) -> str:
        """
        Extrai o áudio de um arquivo (vídeo ou áudio).
        
        Se for áudio, converte para WAV.
        Se for vídeo, extrai o áudio.
        """
        self.logger.info(f"Processando arquivo: {video_path}")
        
        # Verifica se é um arquivo de áudio
        if self._is_audio_file(video_path):
            self.logger.info("Arquivo de áudio detectado. Convertendo para WAV...")
            print(f"{self.colors.CYAN}🎵 Convertendo áudio para WAV...{self.colors.RESET}")
            return self._convert_audio_to_wav(video_path)
        
        # Verifica se é um arquivo de vídeo
        elif self._is_video_file(video_path):
            self.logger.info("Arquivo de vídeo detectado. Extraindo áudio...")
            print(f"{self.colors.CYAN}🎵 Extraindo áudio do vídeo...{self.colors.RESET}")
            return self._extract_audio_from_video(video_path)
        
        else:
            raise ValueError(f"Formato de arquivo não suportado: {video_path}")
    
    def _convert_audio_to_wav(self, audio_path: str) -> str:
        """
        Converte um arquivo de áudio para WAV usando FFmpeg.
        """
        # Cria arquivo temporário para o áudio convertido
        temp_audio = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        try:
            # Usa FFmpeg para converter o áudio
            cmd = [
                'ffmpeg',
                '-i', audio_path,
                '-acodec', 'pcm_s16le',  # Codec WAV
                '-ac', '1',               # Mono
                '-ar', '16000',           # 16kHz (ideal para Whisper)
                temp_audio_path,
                '-y'                      # Sobrescrever se existir
            ]
            
            # Executa o comando
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                # Se FFmpeg falhar, tenta com MoviePy como fallback
                self.logger.warning("FFmpeg falhou, tentando MoviePy...")
                return self._convert_audio_with_moviepy(audio_path)
            
            self.logger.info(f"Áudio convertido para: {temp_audio_path}")
            print(f"{self.colors.GREEN}✅ Áudio convertido com sucesso!{self.colors.RESET}")
            return temp_audio_path
            
        except Exception as e:
            self.logger.error(f"Erro ao converter áudio: {e}")
            # Fallback para MoviePy
            return self._convert_audio_with_moviepy(audio_path)
    
    def _convert_audio_with_moviepy(self, audio_path: str) -> str:
        """Converte áudio usando MoviePy (fallback)."""
        temp_audio = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        try:
            audio = AudioFileClip(audio_path)
            audio.write_audiofile(
                temp_audio_path,
                codec='pcm_s16le',
                fps=16000,
                nbytes=2,
                logger=None
            )
            audio.close()
            
            self.logger.info(f"Áudio convertido para: {temp_audio_path}")
            print(f"{self.colors.GREEN}✅ Áudio convertido com sucesso! (MoviePy){self.colors.RESET}")
            return temp_audio_path
            
        except Exception as e:
            self.logger.error(f"Erro ao converter áudio com MoviePy: {e}")
            raise
    
    def _extract_audio_from_video(self, video_path: str) -> str:
        """Extrai áudio de um arquivo de vídeo."""
        # Cria arquivo temporário para o áudio
        temp_audio = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        try:
            # Primeiro tenta com FFmpeg (mais confiável)
            try:
                cmd = [
                    'ffmpeg',
                    '-i', video_path,
                    '-vn',  # Sem vídeo
                    '-acodec', 'pcm_s16le',
                    '-ac', '1',
                    '-ar', '16000',
                    temp_audio_path,
                    '-y'
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.logger.info(f"Áudio extraído para: {temp_audio_path}")
                    print(f"{self.colors.GREEN}✅ Áudio extraído com sucesso! (FFmpeg){self.colors.RESET}")
                    return temp_audio_path
                else:
                    self.logger.warning("FFmpeg falhou, tentando MoviePy...")
                    
            except Exception as e:
                self.logger.warning(f"FFmpeg não disponível: {e}")
            
            # Fallback para MoviePy
            video = VideoFileClip(video_path)
            audio = video.audio
            
            if audio is None:
                raise ValueError("O vídeo não contém áudio!")
            
            audio.write_audiofile(
                temp_audio_path,
                codec='pcm_s16le',
                fps=16000,
                nbytes=2,
                logger=None
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
        language: str = None,
        task: str = "transcribe"
    ) -> Optional[str]:
        """
        Transcreve o áudio de um vídeo ou arquivo de áudio.
        
        Args:
            video_path: Caminho do vídeo ou áudio
            output_path: Caminho para salvar a transcrição (opcional)
            model_size: Tamanho do modelo ('tiny', 'base', 'small', 'medium', 'large')
            language: Código do idioma (ex: 'pt', 'en', 'es')
            task: 'transcribe' ou 'translate'
        
        Returns:
            str: Texto transcrito ou None em caso de erro
        """
        temp_audio_path = None
        
        try:
            # 1. Carrega o modelo
            model = self._load_model(model_size)
            
            # 2. Processa o arquivo (extrai ou converte áudio)
            temp_audio_path = self._extract_audio(video_path)
            
            # 3. Transcreve
            self.logger.info("Iniciando transcrição...")
            print(f"{self.colors.CYAN}🤖 Transcrevendo áudio... Isso pode levar alguns minutos...{self.colors.RESET}")
            
            options = {
                'task': task,
                'fp16': False  # Para compatibilidade com CPU
            }
            
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
            print(f"{self.colors.RED}❌ Erro: {e}{self.colors.RESET}")
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