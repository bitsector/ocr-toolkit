#!/usr/bin/env python3
"""
OCR Toolkit API - Main Entry Point

This is the main entry point for the OCR Toolkit API application.
The actual FastAPI server configuration is in fast_api_server.py
"""

import uvicorn

if __name__ == "__main__":
    # Start the development server
    uvicorn.run(
        "fast_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["./"],
    )
