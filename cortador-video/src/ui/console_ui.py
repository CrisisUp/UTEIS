"""Interface com o usuário no terminal."""

import os
from typing import Optional, Tuple
from ui.colors import Colors
from utils.time_utils import TimeUtils


class ConsoleUI:
    """Interface interativa no terminal."""
    
    def __init__(self):
        self.colors = Colors()
        self.time_utils = TimeUtils()
    
    def show_header(self):
        """Mostra o cabeçalho do programa."""
        self._clear_screen()
        print(f"{self.colors.MAGENTA}{self.colors.BOLD}--- 🎬 Ferramenta de Corte de Vídeo ---{self.colors.RESET}")
        print("Este programa permite cortar um segmento de um arquivo de vídeo.")
        print(f"{self.colors.YELLOW}Atenção: O FFmpeg é NECESSÁRIO!{self.colors.RESET}")
        print(f"{self.colors.BLUE}Download: https://ffmpeg.org/download.html{self.colors.RESET}\n")
    
    def show_footer(self):
        """Mostra o rodapé do programa."""
        print(f"\n{self.colors.MAGENTA}👋 Obrigado por usar a ferramenta!{self.colors.RESET}")
        print(f"{self.colors.MAGENTA}--- 🎬 Programa Encerrado ---{self.colors.RESET}")
    
    def prompt_input_video(self) -> Optional[str]:
        """Solicita o caminho do vídeo de entrada."""
        print(f"{self.colors.YELLOW}Dica: Arraste o arquivo para o terminal!{self.colors.RESET}")
        
        while True:
            path = input(f"{self.colors.CYAN}👉 Caminho do vídeo (ou 'sair'): {self.colors.RESET}").strip()
            
            if path.lower() == 'sair':
                return None
            
            if os.path.exists(path):
                return path
            else:
                print(f"{self.colors.RED}❌ Arquivo não encontrado.{self.colors.RESET}")
    
    def show_duration(self, duration: float):
        """Mostra a duração do vídeo."""
        formatted = self.time_utils.format_duration(duration)
        print(f"\n{self.colors.BLUE}🎬 Duração: {self.colors.BOLD}{formatted}{self.colors.RESET} ({duration:.2f}s)")
    
    def prompt_cut_times(self, duration: float) -> Tuple[Optional[float], Optional[float]]:
        """Solicita os tempos de corte."""
        print(f"\n{self.colors.CYAN}Insira os tempos de início e fim (em segundos):{self.colors.RESET}")
        
        while True:
            try:
                # Início
                start_input = input(
                    f"{self.colors.BLUE}⏰ Início (0 a {duration:.2f}s): {self.colors.RESET}"
                ).replace(',', '.').strip()
                
                if start_input.lower() == 'sair':
                    return None, None
                
                start = float(start_input)
                
                if start < 0 or start >= duration:
                    print(f"{self.colors.RED}❌ Início inválido. Deve ser entre 0 e {duration:.2f}s{self.colors.RESET}")
                    continue
                
                # Fim
                end_input = input(
                    f"{self.colors.BLUE}⏱️ Fim ({start:.2f} a {duration:.2f}s): {self.colors.RESET}"
                ).replace(',', '.').strip()
                
                if end_input.lower() == 'sair':
                    return None, None
                
                end = float(end_input)
                
                if end <= start or end > duration:
                    print(f"{self.colors.RED}❌ Fim inválido. Deve ser > {start:.2f}s e ≤ {duration:.2f}s{self.colors.RESET}")
                    continue
                
                return start, end
                
            except ValueError:
                print(f"{self.colors.RED}❌ Digite um número válido.{self.colors.RESET}")
    
    def prompt_output_path(self, suggested: str) -> Optional[str]:
        """Solicita o caminho de saída."""
        print(f"\n{self.colors.CYAN}📁 Caminho de saída:{self.colors.RESET}")
        print(f"   Sugestão: {self.colors.BOLD}{suggested}{self.colors.RESET}")
        
        path = input(f"{self.colors.CYAN}👉 Caminho (ou 'sair' para usar sugestão): {self.colors.RESET}").strip()
        
        if path.lower() == 'sair':
            return None
        
        return path if path else suggested
    
    def show_processing(self):
        """Mostra mensagem de processamento."""
        print(f"\n{self.colors.CYAN}--- Processando corte... Isso pode levar um tempo. ---{self.colors.RESET}")
    
    def show_success(self, output_path: str):
        """Mostra mensagem de sucesso."""
        print(f"{self.colors.GREEN}✅ Corte concluído com sucesso!{self.colors.RESET}")
        print(f"{self.colors.GREEN}🎉 Vídeo salvo em: {self.colors.BOLD}{output_path}{self.colors.RESET}")
    
    def show_error(self, message: str):
        """Mostra mensagem de erro."""
        print(f"{self.colors.RED}❌ {message}{self.colors.RESET}")
    
    def prompt_continue(self) -> bool:
        """Pergunta se deseja continuar."""
        response = input(f"\n{self.colors.CYAN}Deseja cortar outro vídeo? (s/n): {self.colors.RESET}").strip().lower()
        return response == 's'
    
    def _clear_screen(self):
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')