POETRY-RUN=poetry run

.PHONY=help

.PHONY: clean
clean: ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf


###
# Lint section
###
.PHONY: _flake8
_flake8:
	@$(POETRY-RUN) flake8 --show-source .

.PHONY: _isort
_isort:
	@$(POETRY-RUN) isort --diff --check-only src/

.PHONY: _black
_black:
	@$(POETRY-RUN) black --check src/

.PHONY: _isort-fix
_isort-fix:
	@$(POETRY-RUN) isort .

.PHONY: _black_fix
_black_fix:
	@$(POETRY-RUN) black .

.PHONY: _dead_fixtures
_dead_fixtures:
	@$(POETRY-RUN) pytest --dead-fixtures tests/

.PHONY: lint
lint: _flake8 _isort _black _dead_fixtures   ## Check code lint

.PHONY: format-code
format-code: _isort-fix _black_fix  ## Format code


###
# Tests section
###
.PHONY: test ## Run tests
test: clean
	@$(POETRY-RUN) pytest -v tests/ -n auto

.PHONY: test-coverage ## Run tests with coverage output
test-coverage: clean
	@$(POETRY-RUN) pytest tests/ --cov . --cov-report term-missing --cov-report xml --cov-report html -n auto

.PHONY: test-debug ## Run tests with active pdb
test-debug: clean
	@$(POETRY-RUN) pytest -s -x tests/

.PHONY: test-matching ## Run tests by match ex: make test-matching k=name_of_test
test-matching: clean
	@$(POETRY-RUN) pytest -s -k $(k) tests/


###
# Run section
###
.PHONY: run
run:
	python main.py



###
# Docker section
###
.PHONY: docker-prune
docker-prune: ## clean docker
	@docker system prune --all --force --volumes

.PHONY: docker-up-db ## up service db
docker-up-db:
	@docker compose up -d db

.PHONY: docker-up ## up all services
docker-up:
	@docker compose up --build -d

.PHONY: docker-down ## down all services
docker-down:
	@docker compose down --remove-orphans -v
