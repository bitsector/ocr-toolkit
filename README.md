# OCR Toolkit API

A professional FastAPI-based backend for optical character recognition (OCR) operations with automatic OpenAPI documentation generation.

## Project Structure

```
ocr-toolkit/
├── src/ocr-engine/          # All source code and Poetry configuration
│   ├── api/             # API layer
│   │   ├── __init__.py  # API package initialization
│   │   └── endpoints.py # API endpoints and route definitions
│   ├── models/          # Data models and schemas
│   │   └── __init__.py  # Pydantic models for request/response
│   ├── core/            # Business logic layer
│   │   ├── __init__.py  # Service exports
│   │   └── ocr_service.py # OCR and language detection services
│   ├── db/              # Database layer
│   │   └── __init__.py  # Database models and connections (empty for now)
│   ├── cache/           # Caching layer
│   │   └── __init__.py  # Cache utilities (empty for now)
│   ├── main.py          # Main entry point for the application
│   ├── fast_api_server.py  # FastAPI application configuration
│   ├── generate_openapi.py  # Script to auto-generate OpenAPI docs
│   ├── pyproject.toml   # Poetry configuration and dependencies
│   └── poetry.lock      # Locked dependency versions
├── openapi/             # Generated OpenAPI documentation
│   ├── openapi.json     # OpenAPI spec in JSON format
│   └── openapi.yaml     # OpenAPI spec in YAML format
├── sample_files/        # Sample images for testing
└── README.md           # This file
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Poetry (recommended) or pip
- **Tesseract OCR** - Required for text extraction functionality

### Installing Tesseract OCR

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

#### macOS (with Homebrew):
```bash
brew install tesseract
```

#### Windows:
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

### Verify Tesseract Installation:
```bash
tesseract --version
```

### Using Poetry (Recommended)

1. **Navigate to the backend directory:**
   ```bash
   cd src/ocr-engine
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Generate OpenAPI documentation:**
   ```bash
   poetry run python generate_openapi.py
   ```

4. **Start the development server:**
   ```bash
   poetry run uvicorn fast_api_server:app --reload --host 0.0.0.0 --port 8000
   ```

5. **View the API documentation:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

## Development Workflow

This project follows the **API-first development** approach:
1. **Develop FastAPI endpoints** with proper type annotations
2. **Auto-generate OpenAPI documentation** from the FastAPI code
3. **Use the generated docs** for testing and frontend development

## Generated Files

The project automatically generates OpenAPI documentation in the `openapi/` directory:

- `openapi/openapi.yaml` - The OpenAPI 3.0 specification in YAML format
- `openapi/openapi.json` - The OpenAPI 3.0 specification in JSON format
- These files are auto-generated from the FastAPI application code

## API Endpoints

### 1. Extract Text
- **POST** `/extract-text`
- Accepts a file upload (JPEG, PNG, WEBP, PDF)
- Returns extracted text with confidence score

### 2. Detect Language
- **POST** `/detect-language` 
- Accepts a file upload (JPEG, PNG, WEBP, PDF)
- Returns detected languages with confidence scores

## Installation & Setup

### Option 1: Using Poetry (Recommended)

1. **Navigate to the backend directory:**
   ```bash
   cd src/ocr-engine
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Start the development server:**
   ```bash
   poetry run uvicorn fast_api_server:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 2: Using pip

1. **Navigate to the backend directory:**
   ```bash
   cd src/ocr-engine
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn[standard] python-multipart pyyaml
   ```

4. **Start the development server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage

Once the server is running (from either option above), you can:

1. **Access the interactive API documentation:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

2. **View the raw OpenAPI specification:**
   - **JSON format**: http://localhost:8000/openapi.json

3. **Generate static OpenAPI files:**
   ```bash
   # From src/ocr-engine/ directory
   poetry run python generate_openapi.py
   ```
   This creates `openapi/openapi.json` and `openapi/openapi.yaml` files.

## Implementation Notes

The generated FastAPI code provides the structure and endpoint definitions, but the actual OCR implementation needs to be added to the endpoint functions in `main.py`. The functions currently contain `pass` statements as placeholders.

To complete the implementation, you would typically:

1. Add OCR libraries like `tesseract`, `easyocr`, or cloud services
2. Implement file processing logic
3. Add error handling
4. Implement the actual text extraction and language detection algorithms

## Testing

### Running the Server Locally

1. **Generate OpenAPI Schemas (non-blocking):**
   ```bash
   poetry run -C src/ocr-engine python generate_openapi.py --no-server
   ```

2. **Run the Backend Server:**
   ```bash
   poetry run -C src/ocr-engine uvicorn fast_api_server:app --reload --host 0.0.0.0 --port 8000
   ```

   **Note**: If you get Tesseract-related errors, make sure Tesseract OCR is installed on your system (see Prerequisites section).

3. **Health Check with cURL:**
   ```bash
   curl -X GET "http://localhost:8000/health" -H "accept: application/json"
   ```

4. **Verify the server is running:**
   The server will start on `http://localhost:8000` and you should see output like:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

5. **Access the interactive documentation:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

### Testing with cURL Commands

Once the server is running, you can test the endpoints using these curl commands. **Note:** All curl commands should be run from the project root directory to access the `sample_files/` folder.

#### 1. Health Check
```bash
# Test the health endpoint
curl -X GET "http://localhost:8000/health" \
  -H "accept: application/json"

# Expected response:
# {"status":"healthy","timestamp":"2025-07-23T09:58:05.471435"}
```

#### 2. Root Endpoint
```bash
# Test the root endpoint
curl -X GET "http://localhost:8000/" \
  -H "accept: application/json"

# Expected response:
# {"message":"OCR Toolkit API is running","status":"healthy"}
```

#### 3. Extract Text from Image
```bash
# Test extract-text endpoint with a sample image
curl -X POST "http://localhost:8000/extract-text" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_files/it_works_on_my_machine.jpg"

# Expected response (placeholder):
# {
#   "success": true,
#   "extracted_text": "This is placeholder extracted text from file: it_works_on_my_machine.jpg. Implement OCR logic here.",
#   "confidence_score": 0.95,
#   "processing_time": 0.001234
# }
```

#### 4. Detect Language in Image
```bash
# Test detect-language endpoint with a sample image
curl -X POST "http://localhost:8000/detect-language" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_files/brain_buffering.jpeg"

# Expected response (placeholder):
# {
#   "success": true,
#   "detected_languages": [
#     {
#       "language": "English",
#       "language_code": "en",
#       "confidence": 0.98,
#       "text_percentage": 85.5
#     },
#     {
#       "language": "Spanish",
#       "language_code": "es",
#       "confidence": 0.76,
#       "text_percentage": 14.5
#     }
#   ],
#   "primary_language": "English",
#   "processing_time": 0.001876
# }
```

#### 5. Test with Your Own Files
```bash
# Upload your own image file
curl -X POST "http://localhost:8000/extract-text" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg"

# Supported formats: JPEG, PNG, WEBP, PDF
# Maximum file size: 10MB
```

#### 6. Test Error Handling
```bash
# Test with unsupported file format
curl -X POST "http://localhost:8000/extract-text" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/file.txt"

# Expected error response:
# {
#   "detail": "Invalid file format. Only JPEG, PNG, WEBP, and PDF files are supported. Got: text/plain"
# }
```

### Available Sample Files

The project includes several sample images in the `sample_files/` directory:
- `brain_buffering.jpeg`
- `for_money.webp`
- `github_actions.webp`
- `it_works_on_my_machine.jpg`
- `linkedin.webp`
- `stranger_things.webp`
- `weasley.webp`

### Interactive Testing

For easier testing, you can also use the interactive Swagger UI:

1. **Start the server from the backend directory:**
   ```bash
   cd src/ocr-engine
   poetry run uvicorn fast_api_server:app --reload --host 0.0.0.0 --port 8000
   ```
2. **Open your browser to:** http://localhost:8000/docs
3. **Click on any endpoint to expand it**
4. **Click "Try it out"**
5. **Upload a file and click "Execute"**

This provides a user-friendly interface for testing all endpoints without writing curl commands.

## Project Architecture

### FastAPI Application (`src/ocr-engine/fast_api_server.py`)
- **Application factory** - Creates and configures the FastAPI app instance
- **Router integration** - Includes API routes from `api.py`
- **Centralized configuration** - App metadata, CORS, middleware setup

### API Endpoints (`src/ocr-engine/api/endpoints.py`)
- **Health check endpoint** (`/health`) - Service status monitoring
- **Root endpoint** (`/`) - Basic API information
- **Text extraction** (`/extract-text`) - OCR text extraction from images
- **Language detection** (`/detect-language`) - Multi-language detection in images

### Data Models (`src/ocr-engine/models/__init__.py`)
- **Pydantic models** - Request/response validation and documentation
- **Type definitions** - Structured data schemas for API contracts

### Business Logic (`src/ocr-engine/core/ocr_service.py`)
- **OCR Service** - Tesseract-based text extraction from images and PDFs
- **Language Detection Service** - Multi-language detection using langdetect
- **File Validation Service** - File type and size validation
- **Image Processing** - PIL-based image preprocessing for better OCR results
- **PDF Processing** - PyMuPDF integration for PDF text extraction and OCR

### Database Layer (`src/ocr-engine/db/`)
- **Database models** - Data persistence layer (empty for now)
- **Connection management** - Database connectivity utilities

### Caching Layer (`src/ocr-engine/cache/`)
- **Cache utilities** - Performance optimization layer (empty for now)
- **Redis integration** - Future caching implementations

### Main Entry Point (`src/ocr-engine/main.py`)
- **Application entry point** - Starts the uvicorn server
- **Development configuration** - Hot-reload and development settings

### OpenAPI Documentation Generation (`src/ocr-engine/generate_openapi.py`)
- **Auto-generates** `openapi/openapi.json` and `openapi/openapi.yaml`
- **Extracts schema** directly from FastAPI application code
- **Maintains consistency** between implementation and documentation
- **Poetry script integration** via `generate-docs` command

### Dependency Management (`src/ocr-engine/pyproject.toml`)
- **Poetry-based** package and dependency management
- **Development dependencies** (black, isort, pytest, httpx)
- **Production dependencies** (fastapi, uvicorn, python-multipart, pyyaml)
- **Custom scripts** for common development tasks

## CI/CD Pipeline

This project includes a comprehensive GitHub Actions CI/CD pipeline that runs:

- **Linting**: Black (formatting) and isort (import sorting) 
- **Static Analysis**: mypy (type checking)
- **Security**: Bandit (vulnerability scanning)
- **Testing**: pytest with API tests
- **Documentation**: OpenAPI generation validation

See [CI-CD.md](CI-CD.md) for detailed pipeline documentation.

### Development Tools

Run the same checks locally before committing:

```bash
cd src/ocr-engine

# Auto-format code
poetry run black .
poetry run isort . --profile black

# Run all CI checks
poetry run black --check --diff .
poetry run isort --check-only --diff . --profile black
poetry run mypy . --config-file mypy.ini  
poetry run bandit -r . -c .bandit -ll
poetry run pytest -v
poetry run python generate_openapi.py --no-server
```
