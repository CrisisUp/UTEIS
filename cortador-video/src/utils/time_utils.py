"""Utilitários para formatação de tempo."""

class TimeUtils:
    """Utilitários para operações com tempo."""
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Formata duração para HH:MM:SS."""
        total_seconds = int(seconds)
        minutes, seconds_rest = divmod(total_seconds, 60)
        hours, minutes_rest = divmod(minutes, 60)
        return f"{hours:02d}:{minutes_rest:02d}:{seconds_rest:02d}"
    
    @staticmethod
    def parse_time(time_str: str) -> float:
        """Converte string de tempo para segundos."""
        # Suporta HH:MM:SS ou segundos
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            elif len(parts) == 2:  # MM:SS
                return int(parts[0]) * 60 + int(parts[1])
        return float(time_str)