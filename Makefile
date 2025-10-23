.PHONY: prepare-dev
prepare-dev:
	@echo "Preparing your local development environment..."; \
	POETRY_VIRTUALENVS_IN_PROJECT=1 poetry sync --with dev --no-root

.PHONY: lint
lint:
	@tput bold; echo "Running linter..."; tput sgr0; \
	POETRY_DONT_LOAD_DOTENV=1 poetry run ruff check app/

.PHONY: lint-fix
lint-fix:
	@tput bold; echo "Running linter..."; tput sgr0; \
	POETRY_DONT_LOAD_DOTENV=1 poetry run ruff check --fix app/

.PHONY: build-mcp
docker:
	@tput bold; echo "Building a docker image..."; tput sgr0; \
	podman compose build mcp


.PHONY: build
docker:
	@tput bold; echo "Building a docker image..."; tput sgr0; \
	podman compose build

.PHONY: run
run:
	@tput bold; echo "Running a docker image..."; tput sgr0; \
		docker run -it -d --name $(DOCKER_CONTAINER) --restart on-failure --env-file .env -v $(shell pwd)/secrets:/code/secrets -p $(PORT):$(PORT) $(DOCKER_IMAGE)
