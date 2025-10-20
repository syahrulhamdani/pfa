# PFA

Personal Finance Assistant - An agent for managing personal finances.

## Features

- Telegram bot integration
- Structured logging with Loguru
- Configuration management with Pydantic Settings

## Contributing

It uses Python 3.12.x via poetry. For development, make sure you have the following:

* [Poetry](https://github.com/python-poetry/poetry)
* [Pyenv](https://github.com/pyenv/pyenv)
* [Podman](https://github.com/containers/podman)

## Directory Structure

```
├── Makefile           <- Makefile with convenience commands like `make podman` or `make run`
├── README.md          <- The top-level README for developers using this project.
├── pyproject.toml     <- Project configuration file with production and dev packages metadata
|                         (such as pylint / pytest).
├── poetry.lock        <- Lock file for dependencies added by poetry.
|
├── Containerfile      <- Instructions for building the application's Docker container
|
├── .gitignore         <- Specifies which files Git should ignore when tracking changes
|
├── .dockerignore      <- Specifies which files and directories should be excluded from Docker builds
|
└── app                <- Source module for use in this project.
    ├── core               <- Core functionality and utilities used across the application
    |   ├── __init__.py    <- Makes core a Python package and handles imports
    |   ├── config.py      <- Configuration management and environment variables
    |   ├── loggers.py     <- Logging configuration and custom logger setup
    |
    ├── repository         <- Data repository layer
    |   ├── __init__.py    <- Makes repository a Python package
    |   ├── base.py        <- Base repository interface/abstract class
    |   ├── prompt.py      <- Prompt interface
    |   └── storage.py     <- Object storage interface
    |
    ├── services
    |   ├── mcp
    |   |   ├── __init__.py        <- Makes `mcp` a Python package
    |   |   ├── prompts.py         <- MCP Prompts
    |   |   └── resources.py       <- MCP Resources
    |   |
    |   └── __init__.py            <- Makes `services` a Python package
    |
    ├── __init__.py             <- Makes `app` a Python module.
    |
    └── mcp_server.py                 <- Main module that includes all defined endpoints.
```

## Preparation

Follow these steps to start the MCP server:

* Clone the repository: `git clone https://github.com/syahrulhamdani/personal-finance-assistant.git`
* Go into the directory and prepare dev enviornment by running below command.

```
POETRY_VIRTUALEVNS_IN_PROJECT=1 poetry sync --no-root --with dev
```

* Don't forget to setup your `.env` file.
