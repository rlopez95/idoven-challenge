.DEFAULT_GOAL := help 

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the app
	docker build .

.PHONY: install
install: ## Install all dependencies
	poetry install

.PHONY: update
update: ## Update dependencies
	poetry update

.PHONY: up
up:    ## Run the app
	docker compose up --build idoven

.PHONY: down
down: ## Stop and remove all the Docker services, volumes and networks
	docker compose down -v --remove-orphans

.PHONY: dev
dev:    ## Run the server in dev mode
	poetry run uvicorn idoven_app.main:app --reload --host 0.0.0.0 --port 8080

.PHONY: check-format
format-code:
	poetry run black --line-length 120 idoven_app/**/*.py

.PHONY: test-unit
test-unit: ## Run all unit tests
	docker compose run --rm --no-deps idoven poetry run pytest idoven_app/tests/unit

.PHONY: test-integration
test-integration: ## Run all integration tests
	docker compose run --rm idoven poetry run pytest idoven_app/tests/integration

.PHONY: test-acceptance
test-acceptance: ## Run all acceptance tests
	docker compose run --rm idoven poetry run pytest idoven_app/tests/acceptance

.PHONY: test
test: test-unit test-integration test-acceptance