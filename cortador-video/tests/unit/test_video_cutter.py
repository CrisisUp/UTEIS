# tests/unit/test_video_cutter.py
import unittest
from src.core.video_cutter import VideoCutter

class TestVideoCutter(unittest.TestCase):
    """Testes unitários para VideoCutter."""
    
    def setUp(self):
        self.cutter = VideoCutter()
    
    def test_cut_video_success(self):
        """Testa corte bem-sucedido."""
        pass
    
    def test_cut_video_invalid_times(self):
        """Testa corte com tempos inválidos."""
        pass
    
    def test_cut_video_file_not_found(self):
        """Testa corte com arquivo inexistente."""
        pass