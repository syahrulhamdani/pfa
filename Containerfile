FROM python:3.12.8-slim

ARG DEBIAN_FRONTEND=noninteractive \
		MCP_PORT=7001

ENV PIP_NO_CACHE_DIR=1 \
		PIP_DISABLE_PIP_VERSION_CHECK=1 \
		POETRY_VIRTUALENVS_CREATE=1 \
		POETRY_VIRTUALENVS_IN_PROJECT=1 \
		POETRY_CACHE_DIR=/tmp/poetry_cache \
		MCP_PORT=7001

RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y --no-install-recommends \
		apt-utils make kmod libpq-dev gcc ca-certificates libffi-dev \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install -U --no-cache-dir pip \
	&& pip install --no-cache-dir poetry

RUN groupadd -r agent && useradd -rm -u 7723 -g agent agent

USER agent

WORKDIR /code

COPY --chown=agent:agent ./pyproject.toml ./poetry.lock /code/

RUN poetry sync --no-root --only main && rm -rf $POETRY_CACHE_DIR

ENV PATH="/code/.venv/bin:$PATH"

COPY --chown=agent:agent ./app /code/app
COPY --chown=agent:agent ./mcp_server.py /code/

USER agent

CMD ["sh", "-c", "gunicorn mcp_server:app -k uvicorn.workers.UvicornWorker --workers 4 --threads 4 -b 0.0.0.0:$MCP_PORT --access-logfile -"]
