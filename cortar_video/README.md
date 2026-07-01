# 🎬 Ferramenta de Corte de Vídeo

Uma ferramenta interativa de linha de comando para cortar segmentos de arquivos de vídeo de forma simples e rápida.

![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)
![MoviePy 1.0.3](https://img.shields.io/badge/MoviePy-1.0.3-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Índice

Sobre o Projeto
Funcionalidades
Pré-requisitos
Instalação
Como Usar
Exemplo Prático
Solução de Problemas
Estrutura do Código
Contribuição
Licença

## 🎯 Sobre o Projeto

Esta ferramenta foi desenvolvida para permitir que usuários cortem trechos específicos de vídeos sem a necessidade de editores de vídeo complexos. Com uma interface simples e intuitiva no terminal, você pode:

Selecionar qualquer vídeo no seu computador
Definir o ponto de início e fim do corte
Salvar o novo vídeo com apenas o trecho desejado

Ideal para:

Criar clips curtos de vídeos longos
Remover partes indesejadas de vídeos
Extrair momentos específicos para apresentações
Preparar vídeos para redes sociais

## ✨ Funcionalidades

Interface amigável no terminal com cores e feedback visual
Validação automática de arquivos e formatos
Persistência de configurações - lembra do último diretório usado
Suporte a múltiplos formatos (MP4, AVI, MOV, MKV, WEBM, etc.)
Corte preciso com tempos em segundos
Feedback em tempo real do processo de corte
Sugestão inteligente de nome para o arquivo de saída
Loop contínuo para cortar múltiplos vídeos na mesma sessão

## 📦 Pré-requisitos

* ### 1. Python 3.6 ou superior

Verifique se o Python está instalado:

```bash
python --version
# ou
python3 --version
```

Download: python.org

* ### 2. FFmpeg (OBRIGATÓRIO)

O FFmpeg é essencial para o processamento de vídeos. Instale conforme seu sistema operacional:

Windows
Baixe do site oficial: ffmpeg.org
Extraia o arquivo ZIP
Adicione a pasta bin ao PATH do sistema
Vídeo tutorial: YouTube
Verifique a instalação:

```bash
ffmpeg -version
```

* `Linux (Ubuntu/Debian)`

```bash
sudo apt update
sudo apt install ffmpeg
```

* `macOS (com Homebrew)`

```bash
brew install ffmpeg
```

## 🚀 Instalação

* ### Opção 1: Instalação Rápida (Recomendada)

```bash
# Clone o repositório (ou crie um arquivo com o código)
git clone https://github.com/seu-usuario/cortador-video.git
cd cortador-video

# Instale a biblioteca necessária
pip install moviepy==1.0.3

# Execute o programa
python cortar_video.py
```

* ### Opção 2: Usando Pipenv (Ambiente Virtual)

```bash
# Instale o Pipenv
pip install pipenv

# Crie um diretório para o projeto
mkdir cortador-video
cd cortador-video

# Instale as dependências
pipenv install moviepy==1.0.3

# Execute o programa
pipenv run python cortar_video.py
```

* ### Opção 3: Usando UV (Gerenciador rápido)

```bash
# Crie um ambiente virtual
uv venv

# Ative o ambiente (Windows)
.venv\Scripts\activate

# Instale as dependências
uv pip install moviepy==1.0.3

# Execute o programa
python cortar_video.py
```

## 🎮 Como Usar

### Passo a Passo

* **Inicie o programa**

```bash
python cortar_video.py
```

* **Informe o caminho do vídeo**

```text
👉 Digite o caminho completo do arquivo de vídeo de entrada: C:\videos\meu_video.mp4
💡 Dica: No Windows, você pode arrastar o arquivo diretamente para o terminal!
```

* **Veja a duração total do vídeo**

```text
🎬 O vídeo tem uma duração total de: 00:05:30 (330.00 segundos).
```

* **Defina os tempos de corte (em segundos)**

```text
⏰ Digite o tempo de início do corte (0 a 330.00 segundos): 120
⏱️ Digite o tempo de fim do corte (120.00 a 330.00 segundos): 180
📝 Exemplos: 60 = 1 minuto, 120 = 2 minutos, 300 = 5 minutos
```

* **Escolha onde salvar**

```text
📁 Digite o caminho para salvar o vídeo cortado: C:\videos\meu_video_cortado.mp4
💡 Pressione ENTER para usar o nome sugerido automaticamente
```

* **Aguarde o processamento**

```text
--- Processando corte... Isso pode levar um tempo. ---
🔄 Carregando vídeo: 'meu_video.mp4'...
✂️ Cortando vídeo de 00:02:00 a 00:03:00...
💾 Salvando vídeo cortado...
✅ Corte concluído com sucesso!
```

* **Corte mais vídeos ou saia**

```text
Deseja cortar outro vídeo? (s/n): 
```

## 📝 Exemplo Prático

### Cenário: Cortar um vídeo de 8 minutos

Vídeo original: Joy.mp4 (8 minutos e 56 segundos)
Objetivo: Extrair um trecho do segundo 50 ao 120 (1 minuto e 10 segundos)

### Execução

```text
--- 🎬 Ferramenta de Corte de Vídeo ---
👉 Digite o caminho do vídeo: C:\Users\Admin\Videos\Joy.mp4
🎬 Duração total: 00:08:56 (536.94 segundos)
⏰ Início do corte: 50
⏱️ Fim do corte: 120
📁 Salvar como: C:\Users\Admin\Videos\Joy_cortado.mp4
✅ Vídeo cortado salvo com sucesso!
```

### Resultado

* Arquivo original: Joy.mp4 (8m56s, ~100MB)
* Arquivo cortado: Joy_cortado.mp4 (1m10s, ~15MB)

## 🔧 Solução de Problemas

Erro: ModuleNotFoundError: No module named 'moviepy.editor'
Causa: Versão do MoviePy muito recente.

Solução:

```bash
# Desinstale a versão atual
pip uninstall moviepy

# Instale a versão compatível
pip install moviepy==1.0.3
```

Erro: 'VideoFileClip' object has no attribute 'subclip'
Causa: Versão do MoviePy incompatível.

Solução: Instale a versão 1.0.3 conforme acima.

Erro: FFmpeg não encontrado
Causa: FFmpeg não instalado ou não está no PATH.

Soluções:

Instale o FFmpeg conforme instruções acima
Reinicie o terminal após a instalação
Verifique com ffmpeg -version

Erro: Arquivo não encontrado
Causa: Caminho incorreto ou arquivo inexistente.

Solução:

Verifique se o caminho está correto
Use caminhos absolutos (ex: C:\videos\video.mp4)
No Windows, arraste o arquivo para o terminal

Erro: Formato de vídeo não suportado
Causa: Extensão de arquivo não reconhecida.

Solução:

Converta o vídeo para um formato comum (MP4, AVI, MOV, MKV)
Verifique se o FFmpeg suporta o formato

O programa está muito lento

Solução:

Use vídeos menores para testes
Corte trechos mais curtos
Tenha paciência - o processamento depende do tamanho do vídeo

## 📁 Estrutura do Código

```text
cortador-video/
│
├── cortar_video.py          # Programa principal
├── video_cutter_config.json # Configurações salvas (criado automaticamente)
├── README.md                # Este arquivo
└── requirements.txt         # Dependências (opcional)
```

## Principais Funções

Função	Descrição
cortar_video()	Função principal que realiza o corte do vídeo
obter_duracao_video()	Retorna a duração total do vídeo
carregar_config()	Carrega configurações do arquivo JSON
salvar_config()	Salva configurações (último diretório usado)
formatar_duracao()	Converte segundos para HH:MM:SS
limpar_tela()	Limpa o terminal para melhor experiência

## 📦 Dependências

moviepy==1.0.3: Biblioteca principal para manipulação de vídeos
FFmpeg: Motor de processamento de vídeo (necessário externamente)

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

Faça um Fork do projeto
Crie sua branch de feature (git checkout -b feature/AmazingFeature)
Commit suas mudanças (git commit -m 'Add some AmazingFeature')
Push para a branch (git push origin feature/AmazingFeature)
Abra um Pull Request

## 📝 Sugestões de Melhorias

Adicionar suporte a cortes com tempo em formato HH:MM:SS
Adicionar barra de progresso mais detalhada
Permitir cortar múltiplos segmentos de uma vez
Adicionar interface gráfica simples (GUI)
Suporte a mais codecs de vídeo

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🙏 Agradecimentos

MoviePy - Biblioteca incrível para edição de vídeos
FFmpeg - Motor de processamento multimídia
Todos os usuários que testaram e contribuíram com feedback

## 📞 Contato

Dúvidas ou sugestões? Abra uma issue ou entre em contato.
Feito com ❤️ para facilitar o corte de vídeos

## 📌 Notas Adicionais

Arquivo requirements.txt (opcional)
Para facilitar a instalação, crie um arquivo requirements.txt:

```text
moviepy==1.0.3
```

E instale com:

```bash
pip install -r requirements.txt
```

## Dica de Segurança

Sempre faça backup dos vídeos originais antes de cortar. O programa não modifica o arquivo original, apenas cria um novo.

## Formatos Suportados

MP4 (.mp4) ✅
AVI (.avi) ✅
MOV (.mov) ✅
MKV (.mkv) ✅
WEBM (.webm) ✅
FLV (.flv) ✅
WMV (.wmv) ✅
MPEG (.mpeg, .mpg) ✅

## Divirta-se cortando seus vídeos! 🎬✨

uv run python -c "import moviepy; print(moviepy.__version__)"
uv pip install --upgrade pillow
uv pip freeze > requirements.txt

### 🚀 Como Usar (Passos Rápidos)

```bash
# 1. Criar ambiente virtual
uv venv

# 2. Ativar (Windows)
.venv\Scripts\activate

# 3. Instalar dependências
uv pip install moviepy==2.2.1

# 4. Executar programa
python cortar_video.py

# 5. Seguir as instruções no terminal
# - Informar caminho do vídeo
# - Definir início e fim (em segundos)
# - Escolher onde salvar

# 6. Cortar mais vídeos ou sair
```
