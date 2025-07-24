#!/usr/bin/env python3
"""
Auto-generate OpenAPI documentation from FastAPI application
Usage:
  python generate_openapi.py
  poetry run generate-docs
"""

import json
import subprocess
import sys
from pathlib import Path

import yaml

from util.logger import get_cli_logger

# Initialize CLI logger for this script
logger = get_cli_logger(__name__)


def main():
    """Generate OpenAPI documentation in JSON and YAML formats"""

    # Check if --no-server flag is passed
    start_server = "--no-server" not in sys.argv

    logger.info("📚 OpenAPI Documentation Generator")
    logger.info("==================================")

    try:
        # Import dependencies
        try:
            from fast_api_server import app
        except ImportError as e:
            logger.error(f"❌ Error importing dependencies: {e}")
            logger.info("Make sure to run: poetry install")
            return False

        # Get the OpenAPI schema from FastAPI
        logger.info("🔄 Extracting OpenAPI schema from FastAPI application...")
        openapi_schema = app.openapi()

        # Create openapi directory if it doesn't exist
        openapi_dir = Path("../../openapi")
        openapi_dir.mkdir(parents=True, exist_ok=True)

        # Generate JSON file
        json_file = openapi_dir / "openapi.json"
        logger.info(f"📄 Generating {json_file}...")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(openapi_schema, f, indent=2, default=str, ensure_ascii=False)

        # Generate YAML file
        yaml_file = openapi_dir / "openapi.yaml"
        logger.info(f"📄 Generating {yaml_file}...")
        with open(yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(
                openapi_schema,
                f,
                default_flow_style=False,
                sort_keys=False,
                indent=2,
                allow_unicode=True,
            )

        logger.info("✅ OpenAPI documentation generated successfully!")
        logger.info("")
        logger.info("Generated files:")
        logger.info(f"  📄 {json_file} - OpenAPI specification in JSON format")
        logger.info(f"  📄 {yaml_file} - OpenAPI specification in YAML format")
        logger.info("")
        logger.info("To view the documentation:")
        logger.info(
            "  1. Start the server: poetry run uvicorn fast_api_server:app --reload --host 0.0.0.0 --port 8000"
        )
        logger.info("  2. Visit: http://localhost:8000/docs (Swagger UI)")
        logger.info("  3. Visit: http://localhost:8000/redoc (ReDoc)")
        logger.info("  4. API JSON: http://localhost:8000/openapi.json")
        logger.info("")

        # Display some stats
        logger.info("API Summary:")
        logger.info(f"  📊 Title: {openapi_schema.get('info', {}).get('title', 'N/A')}")
        logger.info(
            f"  📊 Version: {openapi_schema.get('info', {}).get('version', 'N/A')}"
        )
        logger.info(f"  📊 Endpoints: {len(openapi_schema.get('paths', {}))}")
        logger.info(
            f"  📊 Models: {len(openapi_schema.get('components', {}).get('schemas', {}))}"
        )

        # Conditionally start the server
        if start_server:
            logger.info("\n🚀 Starting FastAPI server automatically...")
            try:
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "uvicorn",
                        "fast_api_server:app",
                        "--reload",
                        "--host",
                        "0.0.0.0",
                        "--port",
                        "8000",
                    ]
                )
            except KeyboardInterrupt:
                logger.info("\n👋 Server stopped. Goodbye!")
            except Exception as e:
                logger.error(f"\n❌ Error starting server: {e}")
        else:
            logger.info("\n✨ OpenAPI documentation generated successfully!")
            logger.info("💡 Tip: Start the server manually with:")
            logger.info(
                "   poetry run uvicorn fast_api_server:app --reload --host 0.0.0.0 --port 8000"
            )

        return True

    except Exception as e:
        logger.error(f"❌ Error generating OpenAPI documentation: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
