"""Interface com o usuário no terminal."""

import os
from typing import Optional, Tuple
from ui.colors import Colors


class ConsoleUI:
    """Interface interativa no terminal para transcrição de vídeos."""
    
    def __init__(self):
        """Inicializa a interface com as cores."""
        self.colors = Colors()
        self.MODELOS_VALIDOS = ['tiny', 'base', 'small', 'medium', 'large']
        self.IDIOMAS_VALIDOS = ['pt', 'en', 'es', 'fr', 'de', 'it', 'ja', 'zh', 'ru']
        self.AUDIO_EXTENSOES = ['.mp3', '.m4a', '.aac', '.flac', '.ogg', '.wav', '.wma', '.aiff']
        self.VIDEO_EXTENSOES = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm', '.mpeg', '.mpg', '.wmv']
    
    # ==================== MÉTODOS PRINCIPAIS ====================
    
    def show_header(self):
        """Mostra o cabeçalho do programa."""
        self._clear_screen()
        print(f"{self.colors.MAGENTA}{self.colors.BOLD}")
        print("--- 🎤 Ferramenta de Transcrição de Vídeo e Áudio ---")
        print(f"{self.colors.RESET}")
        print("Este programa transcreve o áudio de vídeos ou arquivos de áudio para texto.")
        print("Usa o modelo Whisper da OpenAI para reconhecimento de fala.")
        print(f"{self.colors.YELLOW}Atenção: A primeira execução baixará o modelo!{self.colors.RESET}\n")
    
    def show_footer(self):
        """Mostra o rodapé do programa."""
        print(f"\n{self.colors.MAGENTA}👋 Obrigado por usar a ferramenta!{self.colors.RESET}")
        print(f"{self.colors.MAGENTA}--- 🎤 Programa Encerrado ---{self.colors.RESET}")
    
    # ==================== MÉTODOS DE ENTRADA ====================
    
    def prompt_input_video(self) -> Optional[str]:
        """
        Solicita o caminho do vídeo/áudio de entrada.
        
        Returns:
            str: Caminho do arquivo ou None se o usuário cancelar
        """
        print(f"{self.colors.YELLOW}Dica: Arraste o arquivo para o terminal!{self.colors.RESET}")
        print(f"{self.colors.BLUE}Formatos suportados:{self.colors.RESET}")
        print(f"   Vídeo: {', '.join(self.VIDEO_EXTENSOES)}")
        print(f"   Áudio: {', '.join(self.AUDIO_EXTENSOES)}")
        
        while True:
            path = input(f"\n{self.colors.CYAN}👉 Caminho do arquivo (ou 'sair'): {self.colors.RESET}").strip()
            
            if path.lower() == 'sair':
                return None
            
            if not path:
                print(f"{self.colors.RED}❌ Caminho vazio. Digite um caminho válido.{self.colors.RESET}")
                continue
            
            # Remove aspas
            path = path.strip('"\'')
            
            if os.path.exists(path):
                return path
            else:
                print(f"{self.colors.RED}❌ Arquivo não encontrado. Verifique o caminho.{self.colors.RESET}")
    
    def prompt_model_size(self) -> str:
        """
        Solicita o tamanho do modelo Whisper.
        
        Returns:
            str: Tamanho do modelo escolhido
        """
        print(f"\n{self.colors.CYAN}📊 Tamanho do modelo Whisper:{self.colors.RESET}")
        print("   tiny   - Mais rápido, menos preciso")
        print("   base   - Bom equilíbrio (recomendado)")
        print("   small  - Melhor precisão, mais lento")
        print("   medium - Alta precisão, lento")
        print("   large  - Máxima precisão, muito lento")
        
        while True:
            choice = input(f"{self.colors.BLUE}👉 Escolha (tiny/base/small/medium/large): {self.colors.RESET}").strip().lower()
            
            if not choice:
                print(f"{self.colors.YELLOW}Usando modelo 'base' (recomendado){self.colors.RESET}")
                return 'base'
            
            if choice in self.MODELOS_VALIDOS:
                return choice
            else:
                print(f"{self.colors.RED}❌ Opção inválida. Escolha entre: {', '.join(self.MODELOS_VALIDOS)}{self.colors.RESET}")
    
    def prompt_language(self) -> Optional[str]:
        """
        Solicita o idioma do áudio.
        
        Returns:
            str: Código do idioma ou None para detecção automática
        """
        print(f"\n{self.colors.CYAN}🌐 Idioma do áudio:{self.colors.RESET}")
        print("   pt - Português")
        print("   en - Inglês")
        print("   es - Espanhol")
        print("   fr - Francês")
        print("   de - Alemão")
        print("   it - Italiano")
        print("   ja - Japonês")
        print("   zh - Chinês")
        print("   ru - Russo")
        print("   (Enter) - Detectar automaticamente")
        
        lang = input(f"{self.colors.BLUE}👉 Código do idioma (ou Enter para automático): {self.colors.RESET}").strip().lower()
        
        if lang == '':
            return None
        
        if lang in self.IDIOMAS_VALIDOS:
            return lang
        else:
            print(f"{self.colors.YELLOW}⚠️ Idioma não reconhecido. Usando detecção automática.{self.colors.RESET}")
            return None
    
    def prompt_translate(self) -> bool:
        """
        Pergunta se deseja traduzir para inglês.
        
        Returns:
            bool: True se quiser traduzir, False caso contrário
        """
        print(f"\n{self.colors.CYAN}🔄 Opção de tradução:{self.colors.RESET}")
        print("   Transcrever no idioma original (recomendado)")
        print("   Traduzir para inglês")
        
        choice = input(f"{self.colors.BLUE}👉 Traduzir para inglês? (s/n) [n]: {self.colors.RESET}").strip().lower()
        return choice == 's'
    
    def prompt_output_path(self, video_path: str) -> Optional[str]:
        """
        Solicita o caminho de saída para a transcrição.
        
        Args:
            video_path: Caminho do vídeo de entrada
        
        Returns:
            str: Caminho de saída ou None se o usuário cancelar
        """
        # Gera caminho sugerido com extensão .txt
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        default_output = os.path.join(
            os.path.dirname(video_path) or '.',
            f"{base_name}_transcricao.txt"
        )
        
        print(f"\n{self.colors.CYAN}📁 Caminho de saída:{self.colors.RESET}")
        print(f"   Sugestão: {self.colors.BOLD}{default_output}{self.colors.RESET}")
        print(f"   {self.colors.YELLOW}💡 Use .txt para arquivos de texto{self.colors.RESET}")
        
        path = input(f"{self.colors.CYAN}👉 Caminho (ou 'sair' para usar sugestão): {self.colors.RESET}").strip()
        
        if path.lower() == 'sair':
            return None
        
        # Usa a sugestão se o usuário não digitou nada
        if not path:
            return default_output
        
        # Valida e corrige a extensão
        path = self._validate_output_path(path)
        
        return path
    
    def prompt_overwrite(self, file_path: str) -> bool:
        """
        Pergunta se deve sobrescrever um arquivo existente.
        
        Args:
            file_path: Caminho do arquivo que já existe
        
        Returns:
            bool: True se quiser sobrescrever, False caso contrário
        """
        print(f"\n{self.colors.YELLOW}⚠️ O arquivo já existe: {file_path}{self.colors.RESET}")
        choice = input(f"{self.colors.CYAN}👉 Sobrescrever? (s/n): {self.colors.RESET}").strip().lower()
        return choice == 's'
    
    def prompt_extra_formats(self) -> bool:
        """
        Pergunta se deseja salvar em formatos adicionais.
        
        Returns:
            bool: True se quiser formatos adicionais, False caso contrário
        """
        print(f"\n{self.colors.CYAN}📄 Formatos adicionais:{self.colors.RESET}")
        print("   Salvar também em SRT (legendas) e JSON?")
        choice = input(f"{self.colors.BLUE}👉 Salvar formatos adicionais? (s/n) [n]: {self.colors.RESET}").strip().lower()
        return choice == 's'
    
    def prompt_continue(self) -> bool:
        """
        Pergunta se o usuário deseja continuar.
        
        Returns:
            bool: True se quiser continuar, False caso contrário
        """
        response = input(f"\n{self.colors.CYAN}Deseja transcrever outro arquivo? (s/n): {self.colors.RESET}").strip().lower()
        return response == 's'
    
    # ==================== MÉTODOS DE SAÍDA ====================
    
    def show_file_info(self, file_path: str):
        """
        Mostra informações do arquivo.
        
        Args:
            file_path: Caminho do arquivo
        """
        import os
        from datetime import datetime
        
        size = os.path.getsize(file_path)
        size_mb = size / (1024 * 1024)
        
        # Determina o tipo de arquivo
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in self.AUDIO_EXTENSOES:
            file_type = "Áudio"
        elif ext in self.VIDEO_EXTENSOES:
            file_type = "Vídeo"
        else:
            file_type = "Desconhecido"
        
        print(f"\n{self.colors.BLUE}📁 Informações do arquivo:{self.colors.RESET}")
        print(f"   Nome: {os.path.basename(file_path)}")
        print(f"   Tipo: {file_type} ({ext})")
        print(f"   Tamanho: {size_mb:.2f} MB")
        print(f"   Modificado: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d/%m/%Y %H:%M')}")
    
    def show_processing(self):
        """Mostra mensagem de processamento."""
        print(f"\n{self.colors.CYAN}--- Processando transcrição... Isso pode levar alguns minutos. ---{self.colors.RESET}")
    
    def show_success(self, output_path: str):
        """
        Mostra mensagem de sucesso.
        
        Args:
            output_path: Caminho do arquivo gerado
        """
        print(f"\n{self.colors.GREEN}✅ Transcrição concluída com sucesso!{self.colors.RESET}")
        print(f"{self.colors.GREEN}📄 Arquivo salvo em: {self.colors.BOLD}{output_path}{self.colors.RESET}")
    
    def show_preview(self, text: str, max_chars: int = 500):
        """
        Mostra um preview da transcrição.
        
        Args:
            text: Texto da transcrição
            max_chars: Número máximo de caracteres no preview
        """
        print(f"\n{self.colors.CYAN}📝 Preview da transcrição:{self.colors.RESET}")
        print("-" * 60)
        
        # Mostra apenas os primeiros max_chars caracteres
        preview = text[:max_chars]
        if len(text) > max_chars:
            preview += "..."
        
        print(preview)
        print("-" * 60)
        
        # Estatísticas do texto
        palavras = len(text.split())
        print(f"{self.colors.YELLOW}Total: {len(text)} caracteres, {palavras} palavras{self.colors.RESET}")
    
    def show_extra_formats_saved(self, formats: list):
        """
        Mostra que formatos adicionais foram salvos.
        
        Args:
            formats: Lista de caminhos dos arquivos salvos
        """
        print(f"\n{self.colors.GREEN}📄 Formatos adicionais salvos:{self.colors.RESET}")
        for f in formats:
            print(f"   ✅ {f}")
    
    def show_error(self, message: str):
        """
        Mostra mensagem de erro.
        
        Args:
            message: Mensagem de erro
        """
        print(f"{self.colors.RED}❌ {message}{self.colors.RESET}")
    
    def show_warning(self, message: str):
        """
        Mostra mensagem de aviso.
        
        Args:
            message: Mensagem de aviso
        """
        print(f"{self.colors.YELLOW}⚠️ {message}{self.colors.RESET}")
    
    def show_info(self, message: str):
        """
        Mostra mensagem informativa.
        
        Args:
            message: Mensagem informativa
        """
        print(f"{self.colors.CYAN}ℹ️ {message}{self.colors.RESET}")
    
    def show_duration(self, duration: float):
        """
        Mostra a duração do vídeo/áudio.
        
        Args:
            duration: Duração em segundos
        """
        from utils.time_utils import TimeUtils  # Importação local para evitar dependência circular
        formatted = TimeUtils.format_duration(duration)
        print(f"\n{self.colors.BLUE}⏱️ Duração: {self.colors.BOLD}{formatted}{self.colors.RESET}")
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _validate_output_path(self, path: str) -> str:
        """
        Valida e corrige a extensão do caminho de saída.
        
        Args:
            path: Caminho de saída
        
        Returns:
            str: Caminho com extensão .txt garantida
        """
        # Remove extensões de vídeo/áudio ou outras extensões indesejadas
        base, ext = os.path.splitext(path)
        
        # Se a extensão não for .txt, força .txt
        if ext.lower() != '.txt':
            # Se não tem extensão ou tem extensão de vídeo/áudio, adiciona .txt
            if not ext or ext.lower() in self.VIDEO_EXTENSOES + self.AUDIO_EXTENSOES:
                path = f"{base}.txt"
                self.show_warning(f"Extensão corrigida para .txt: {path}")
        
        return path
    
    def _clear_screen(self):
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_file_type(self, file_path: str) -> str:
        """
        Retorna o tipo do arquivo.
        
        Args:
            file_path: Caminho do arquivo
        
        Returns:
            str: 'video', 'audio' ou 'unknown'
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in self.VIDEO_EXTENSOES:
            return 'video'
        elif ext in self.AUDIO_EXTENSOES:
            return 'audio'
        else:
            return 'unknown'