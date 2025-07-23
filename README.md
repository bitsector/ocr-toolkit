# OCR Toolkit API

A professional FastAPI-based backend for optical character recognition (OCR) operations with automatic OpenAPI documentation generation.

## Project Structure

```
ocr-toolkit/
├── src/backend/          # All source code and Poetry configuration
│   ├── main.py          # FastAPI application with endpoints
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

### Using Poetry (Recommended)

1. **Navigate to the backend directory:**
   ```bash
   cd src/backend
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
   poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
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
   cd src/backend
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Start the development server:**
   ```bash
   poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 2: Using pip

1. **Navigate to the backend directory:**
   ```bash
   cd src/backend
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
   # From src/backend/ directory
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
   poetry run -C src/backend python generate_openapi.py --no-server
   ```

2. **Run the Backend Server:**
   ```bash
   poetry run -C src/backend uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

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
   cd src/backend
   poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
2. **Open your browser to:** http://localhost:8000/docs
3. **Click on any endpoint to expand it**
4. **Click "Try it out"**
5. **Upload a file and click "Execute"**

This provides a user-friendly interface for testing all endpoints without writing curl commands.

## Project Architecture

### FastAPI Application (`src/backend/main.py`)
- **Health check endpoint** (`/health`) - Service status monitoring
- **Root endpoint** (`/`) - Basic API information
- **Text extraction** (`/extract-text`) - OCR text extraction from images
- **Language detection** (`/detect-language`) - Multi-language detection in images
- **Automatic OpenAPI schema generation** with proper type annotations

### OpenAPI Documentation Generation (`src/backend/generate_openapi.py`)
- **Auto-generates** `openapi/openapi.json` and `openapi/openapi.yaml`
- **Extracts schema** directly from FastAPI application code
- **Maintains consistency** between implementation and documentation
- **Poetry script integration** via `generate-docs` command

### Dependency Management (`src/backend/pyproject.toml`)
- **Poetry-based** package and dependency management
- **Development dependencies** (black, isort, pytest, httpx)
- **Production dependencies** (fastapi, uvicorn, python-multipart, pyyaml)
- **Custom scripts** for common development tasks

---

*Professional OCR API with auto-generated documentation*
