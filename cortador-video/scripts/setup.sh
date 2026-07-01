#!/bin/bash
# Script de instalação para Linux/Mac

echo "🎬 Instalando Cortador de Vídeo"

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale o Python 3.8+"
    exit 1
fi

# Verifica UV
if ! command -v uv &> /dev/null; then
    echo "📦 Instalando UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Cria ambiente virtual
echo "🔧 Criando ambiente virtual..."
uv venv

# Ativa ambiente
source .venv/bin/activate

# Instala dependências
echo "📦 Instalando dependências..."
uv pip install -r requirements.txt

# Verifica FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg não encontrado!"
    echo "   Instale o FFmpeg: https://ffmpeg.org/download.html"
fi

echo "✅ Instalação concluída!"
echo "🚀 Para executar: python src/main.py"