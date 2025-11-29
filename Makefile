.PHONY: help install test lint run clean

help:
	@echo "Comandos disponibles:"
	@echo "  make install    - Instalar dependencias"
	@echo "  make test       - Ejecutar pruebas"
	@echo "  make lint       - Ejecutar linting"
	@echo "  make run        - Ejecutar aplicación"
	@echo "  make clean      - Limpiar archivos temporales"

install:
	pip install -r requirements.txt

test:
	pytest --cov=. --cov-report=html --cov-report=term

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

run:
	python app.py

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build


