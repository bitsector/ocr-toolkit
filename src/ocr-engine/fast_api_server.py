from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="OCR Toolkit API",
        description="API for optical character recognition operations including text extraction and language detection",
        version="1.0.0",
        contact={"name": "OCR Toolkit", "email": "support@ocr-toolkit.com"},
        license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    )

    # Import and include API routes
    from api.endpoints import router

    app.include_router(router)

    return app


# Create the app instance
app = create_app()
