# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Speedtest All-In-One is a containerized application that automatically captures Ookla Speedtest metrics and displays them in a Grafana dashboard. The system consists of:

1. **Python speedtest script**: Runs periodically via cron to capture speedtest data
2. **SQLite database**: Stores speedtest results with persistent storage via Docker volumes
3. **Grafana dashboard**: Visualizes the speedtest metrics over time

## Development Commands

### Poetry Environment Setup
```bash
# Install dependencies (main only)
poetry install --only main

# Install all dependencies including dev
poetry install
```

### Testing
```bash
# Run all tests with coverage
coverage run -m pytest --color=yes -vvv

# Generate coverage report
coverage report

# Run a single test file
pytest tests/test_class_Config.py -vvv

# Run a specific test function
pytest tests/test_class_Config.py::test_config -vvv
```

### Code Quality Tools
The project uses multiple linters and formatters. Run them in this order:

```bash
# Format code with Black (line length: 120)
black --config pyproject.toml .

# Sort imports with isort (black profile)
find . -name '*.py' -not -path '*/tests/*' | xargs isort --profile black --skip tests/

# Run Flake8 linter
flake8p --config pyproject.toml .

# Run Pylint
find . -name '*.py' | xargs pylint --rcfile=pyproject.toml

# Run pydocstyle (Google convention)
pydocstyle . --config=pyproject.toml

# Run Bandit security scanner
bandit --recursive ./ --configfile pyproject.toml
```

### Docker Commands
All commands must be run from the repository root:

```bash
# Build Docker images
docker-compose build

# Start the application
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f speedtest_aio

# Remove intermediate build images
docker image prune --filter "label=prune=true"

# Wipe dashboard data (requires down first)
docker volume rm speedtest_aio_grafana-storage speedtest_aio_speedtest-storage
```

### Raspberry Pi Support
For Raspberry Pi deployments, use the `-RPi` variants:
```bash
docker-compose -f docker-compose-RPi.yml build
docker-compose -f docker-compose-RPi.yml up -d
```

## Architecture

### Multi-Stage Docker Build
The Dockerfile uses a three-stage build process:
1. **base**: Installs Poetry and main dependencies
2. **test**: Runs all linters, formatters, and tests
3. **cli**: Final slim image with Supercronic for cron scheduling

### Database Schema
SQLite table `speedtest` with columns:
- `test_id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `timestamp`: INTEGER (epoch time in seconds)
- `download`: INTEGER (bits per second)
- `upload`: INTEGER (bits per second)
- `ping`: FLOAT (milliseconds)
- `server_id`: INTEGER
- `server_host`: TEXT

### Application Flow
1. Container starts with `entrypoint.sh` which launches Supercronic
2. Supercronic executes `speedtest_aio.py` based on `crontab` schedule (default: every 15 minutes)
3. Script runs `speedtest --secure --json` via subprocess
4. Results are parsed and inserted into SQLite database at `/app/db/speedtest_database.sqlite`
5. Grafana reads from the shared database volume using the sqlite-datasource plugin

### Configuration
- **Environment Variables**: `LOG_LEVEL` (default: INFO), `LOG_PATH` (default: log/)
- **Cron Schedule**: Edit `crontab` file (use crontab.guru for syntax help)
- **Grafana Thresholds**: Modify panel overrides in Grafana UI to match your connection speed

### Key Dependencies
- `speedtest-cli`: Python wrapper for Ookla Speedtest CLI
- Python 3.12 or 3.13 (>=3.12,<3.14)

`CustomLogger` and `pretty_print` were previously imported from the external
`aaron-common-libs` package. As of 0.8.0 they live in this repo at
`speedtest_aio/logger/custom_logger.py` and `speedtest_aio/common_funcs.py`;
the external dependency is gone.

### Test Configuration
Tests are configured via `[tool.pytest.ini_options]` in pyproject.toml:
- Sets `LOG_LEVEL=DEBUG` and `LOG_PATH=/tmp/` for test runs
- Uses Google docstring convention for pydocstyle
- Bandit skips subprocess warnings (B404, B603) as intentional

## Important Notes

- The speedtest binary path is hardcoded to `/usr/local/bin/speedtest` in speedtest_aio.py:150
- Database file path is hardcoded to `/app/db/speedtest_database.sqlite` in speedtest_aio.py:160
- Grafana is accessible at http://localhost:3000 (default: admin/admin)
- Dashboard data persists across container restarts via Docker volumes
- All datetime values are converted to epoch integers for Grafana compatibility
