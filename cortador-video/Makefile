.PHONY: help install dev-install test lint format clean run

help:
	@echo "Comandos disponíveis:"
	@echo "  make install       - Instala dependências"
	@echo "  make dev-install   - Instala dependências de desenvolvimento"
	@echo "  make test          - Executa testes"
	@echo "  make lint          - Executa linters"
	@echo "  make format        - Formata código"
	@echo "  make clean         - Limpa arquivos temporários"
	@echo "  make run           - Executa o programa"

install:
	uv pip install -r requirements.txt

dev-install:
	uv pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src/
	pylint src/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/

run:
	python src/main.py