# CI/CD Pipeline

This document describes the GitHub Actions CI/CD pipeline for the OCR Toolkit project.

## Pipeline Overview

The CI/CD pipeline is defined in `.github/workflows/ci-cd.yml` and consists of 6 separate jobs that run in a specific order:

### 1. Lint Job
- **Black**: Code formatting check
- **isort**: Import sorting check
- Runs independently and must pass before build/test jobs

### 2. Static-Check Job  
- **mypy**: Static type checking
- Runs independently and must pass before build/test jobs

### 3. Security-Check Job
- **Bandit**: Security vulnerability scanning
- **Trivy**: Filesystem vulnerability scanning
- Runs independently and must pass before build/test jobs

### 4. Build Job
- **Dependencies**: [lint, static-check, security-check] 
- **Server startup test**: Verifies the FastAPI server starts correctly
- **OpenAPI generation test**: Validates OpenAPI documentation generation

### 5. Test Job
- **Dependencies**: [lint, static-check, security-check]
- **pytest**: Unit and integration tests
- Runs in parallel with build job

### 6. Integration-Test Job
- **Dependencies**: [build, test]
- Runs only on main branch pushes
- Tests the API with actual sample image files
- Validates OCR functionality end-to-end

## Python Version

- **Target Version**: Python 3.13
- All jobs use the same Python version for consistency
- Removed matrix testing to focus on single version

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

- **Single Version**: Python 3.13 only
- **Platform**: Ubuntu latest
- **Reasoning**: Simplified for consistency and faster builds

## Job Dependencies

```
lint ──┐
       ├── build ──┐
static-check ──┤           ├── integration-test
       ├── test ───┘
security-check ──┘
```

- Lint, static-check, and security-check run in parallel
- Build and test jobs wait for all three to complete
- Integration-test waits for both build and test to complete

## Artifacts

The pipeline generates:
- Bandit security scan reports
- Trivy vulnerability scan results (uploaded to GitHub Security tab)
- OpenAPI documentation files
- Test coverage reports (if configured)

## Secrets and Variables

No secrets are currently required for the pipeline. All tools run against the public codebase.

## Failure Handling

- **Lint failures**: Pipeline fails if code doesn't meet formatting standards
- **Test failures**: Pipeline fails if any tests don't pass
- **Security issues**: High severity issues fail the pipeline, low/medium issues generate warnings
- **Build failures**: Pipeline fails if OpenAPI generation or server startup fails
