# CI/CD Pipeline

This document describes the GitHub Actions CI/CD pipeline for the OCR Toolkit project.

## Pipeline Overview

The CI/CD pipeline is defined in `.github/workflows/ci-cd.yml` and consists of 4 main jobs:

### 1. Lint and Security (lint-and-security)
- **Black**: Code formatting check
- **isort**: Import sorting check  
- **mypy**: Static type checking
- **Bandit**: Security vulnerability scanning

### 2. Test and Build (test-and-build)
- **pytest**: Unit and integration tests
- **Server startup test**: Verifies the FastAPI server starts correctly
- **OpenAPI generation test**: Validates OpenAPI documentation generation

### 3. Integration Test (integration-test)
- Runs only on main branch pushes
- Tests the API with actual sample image files
- Validates OCR functionality end-to-end

### 4. Security Scan (security-scan)
- **Trivy**: Filesystem vulnerability scanning
- Uploads results to GitHub Security tab

## Tools Configuration

### Black (Code Formatting)
- Uses default Black configuration
- Line length: 88 characters
- Applied to all Python files

### isort (Import Sorting)  
- Profile: "black" (compatible with Black formatter)
- Configuration in `pyproject.toml`

### mypy (Static Type Checking)
- Configuration in `mypy.ini`
- Ignores missing imports for external libraries
- Type ignore comments used where needed

### Bandit (Security)
- Configuration in `.bandit` 
- Excludes test directories
- Skips B104 (bind all interfaces) for development servers

### pytest (Testing)
- Test files in `tests/` directory
- Includes API endpoint tests
- Uses FastAPI TestClient

## Local Development

Run the same checks locally:

```bash
cd src/backend

# Format code
poetry run black .
poetry run isort . --profile black

# Run checks (same as CI)
poetry run black --check --diff .
poetry run isort --check-only --diff . --profile black  
poetry run mypy . --config-file mypy.ini
poetry run bandit -r . -c .bandit -ll
poetry run pytest -v
poetry run python generate_openapi.py --no-server
```

## Triggering the Pipeline

The pipeline runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

## Matrix Testing

Tests run on Python versions:
- 3.10
- 3.11  
- 3.12

## Artifacts

The pipeline generates:
- Bandit security scan reports
- OpenAPI documentation files
- Test coverage reports (if configured)

## Secrets and Variables

No secrets are currently required for the pipeline. All tools run against the public codebase.

## Failure Handling

- **Lint failures**: Pipeline fails if code doesn't meet formatting standards
- **Test failures**: Pipeline fails if any tests don't pass
- **Security issues**: High severity issues fail the pipeline, low/medium issues generate warnings
- **Build failures**: Pipeline fails if OpenAPI generation or server startup fails
