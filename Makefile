# Makefile для Instagram Profile Parser

.PHONY: help install install-dev test lint format clean build upload

# Переменные
PYTHON := python3
PIP := pip3
PACKAGE_NAME := instagram-profile-parser

help:  ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Установить зависимости
	$(PIP) install -r requirements.txt

install-dev:  ## Установить зависимости для разработки
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

test:  ## Запустить тесты
	$(PYTHON) -m pytest tests/ -v

lint:  ## Проверить код линтерами
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy .

format:  ## Форматировать код
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

clean:  ## Очистить временные файлы
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

build: clean  ## Собрать пакет
	$(PYTHON) setup.py sdist bdist_wheel

upload: build  ## Загрузить пакет в PyPI
	twine upload dist/*

setup-env:  ## Настроить виртуальное окружение
	$(PYTHON) -m venv venv
	@echo "Активируйте виртуальное окружение:"
	@echo "source venv/bin/activate  # Linux/Mac"
	@echo "venv\\Scripts\\activate     # Windows"

run-example:  ## Запустить пример использования
	$(PYTHON) -m instagram_parser.cli --help

check-deps:  ## Проверить зависимости
	$(PIP) check

update-deps:  ## Обновить зависимости
	$(PIP) install --upgrade -r requirements.txt

security-check:  ## Проверить безопасность
	$(PIP) install safety
	safety check

docs:  ## Создать документацию
	@echo "Создание документации..."
	@echo "Документация будет доступна в docs/"

docker-build:  ## Собрать Docker образ
	docker build -t $(PACKAGE_NAME) .

docker-run:  ## Запустить в Docker
	docker run -it --rm $(PACKAGE_NAME)

# Команды для разработки
dev-setup: install-dev  ## Настроить окружение для разработки
	pre-commit install

pre-commit:  ## Запустить pre-commit проверки
	pre-commit run --all-files

# Команды для CI/CD
ci-test:  ## Запустить тесты для CI
	$(PYTHON) -m pytest tests/ --cov=instagram_parser --cov-report=xml

ci-lint:  ## Запустить линтеры для CI
	$(PYTHON) -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	$(PYTHON) -m mypy . --ignore-missing-imports
