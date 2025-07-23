# A FastAPI-based backend for optical character recognition (OCR) operations.

## Quick Start

### Using Poetry (Recommended)

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Generate OpenAPI documentation:**
   ```bash
   ./generate_openapi.sh
   ```
   Or manually:
   ```bash
   poetry run python generate_openapi.py
   ```

3. **Start the development server:**
   ```bash
   poetry run start
   ```

4. **View the API documentation:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

## Development Workflow

This project follows the **API-first development** approach:
1. **Develop FastAPI endpoints** with proper type annotations
2. **Auto-generate OpenAPI documentation** from the FastAPI code
3. **Use the generated docs** for testing and frontend development API

A FastAPI-based backend for optical character recognition (OCR) operations.

## Generated Files

This project was generated from an OpenAPI specification and includes:

- `openapi.yaml` - The OpenAPI 3.0 specification defining the API endpoints
- `main.py` - FastAPI application with endpoint definitions
- `models.py` - Pydantic models for request/response validation
- `requirements.txt` - Python dependencies
- `start_server.sh` - Script to start the development server

## API Endpoints

### 1. Extract Text
- **POST** `/extract-text`
- Accepts a file upload (JPEG, PNG, WEBP, PDF)
- Returns extracted text with confidence score

### 2. Detect Language
- **POST** `/detect-language` 
- Accepts a file upload (JPEG, PNG, WEBP, PDF)
- Returns detected languages with confidence scores

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the development server:
```bash
./start_server.sh
```

Or manually:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

Once the server is running, you can:

1. Access the API documentation at: http://localhost:8000/docs
2. View the OpenAPI spec at: http://localhost:8000/openapi.json

## Implementation Notes

The generated FastAPI code provides the structure and endpoint definitions, but the actual OCR implementation needs to be added to the endpoint functions in `main.py`. The functions currently contain `pass` statements as placeholders.

To complete the implementation, you would typically:

1. Add OCR libraries like `tesseract`, `easyocr`, or cloud services
2. Implement file processing logic
3. Add error handling
4. Implement the actual text extraction and language detection algorithms

## Testing

### Running the Server Locally

1. **Start the development server:**
   ```bash
   # Using Poetry (recommended)
   poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Or using the Poetry script
   poetry run start
   ```

2. **Verify the server is running:**
   The server will start on `http://localhost:8000` and you should see output like:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

3. **Access the interactive documentation:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

### Testing with cURL Commands

Once the server is running, you can test the endpoints using these curl commands:

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

1. Start the server: `poetry run uvicorn main:app --reload`
2. Open your browser to: http://localhost:8000/docs
3. Click on any endpoint to expand it
4. Click "Try it out"
5. Upload a file and click "Execute"

This provides a user-friendly interface for testing all endpoints without writing curl commands.

---

*Cutting edge of OCR capabilities API*
