"""Exceções personalizadas para o cortador de vídeo."""

class VideoCutterError(Exception):
    """Exceção base para erros do cortador de vídeo."""
    pass


class VideoNotFoundError(VideoCutterError):
    """Exceção levantada quando o arquivo de vídeo não é encontrado."""
    pass


class InvalidVideoFormatError(VideoCutterError):
    """Exceção levantada quando o formato do vídeo não é suportado."""
    pass


class InvalidCutTimesError(VideoCutterError):
    """Exceção levantada quando os tempos de corte são inválidos."""
    pass


class VideoProcessingError(VideoCutterError):
    """Exceção levantada quando ocorre um erro no processamento do vídeo."""
    pass


class FFmpegNotFoundError(VideoCutterError):
    """Exceção levantada quando o FFmpeg não é encontrado."""
    pass