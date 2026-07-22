# =============================================
# Web-Scrape-Notifier - Makefile
# =============================================

.PHONY: help test build up down logs clean

# Default target
help:
	@echo "🕷️  Web-Scrape-Notifier - Available commands:"
	@echo ""
	@echo "  make help           - Show this help message!  (ᵔᵕᵔ)ﾉ"
	@echo "  make test           - Run unit tests locally"
	@echo "  make build          - Build docker image"
	@echo "  make up             - Start the docker container"
	@echo "  make down           - Stop the docker container"
	@echo "  make logs           - View container logs"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""

test:
	python -m unittest discover -s tests -v

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v --rmi local

restart: 
	$(MAKE) down
	$(MAKE) build
	$(MAKE) up
