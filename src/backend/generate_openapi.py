#!/usr/bin/env python3
"""
Auto-generate OpenAPI documentation from FastAPI application
Usage: 
  python generate_openapi.py
  poetry run generate-docs
"""

import json
import sys
from pathlib import Path

def main():
    """Generate OpenAPI documentation in JSON and YAML formats"""
    
    # Check if --no-server flag is passed
    start_server = "--no-server" not in sys.argv
    
    print("📚 OpenAPI Documentation Generator")
    print("==================================")
    
    try:
        # Import dependencies
        try:
            import yaml
            from fast_api_server import app
        except ImportError as e:
            print(f"❌ Error importing dependencies: {e}")
            print("Make sure to run: poetry install")
            return False
        
        # Get the OpenAPI schema from FastAPI
        print("🔄 Extracting OpenAPI schema from FastAPI application...")
        openapi_schema = app.openapi()
        
        # Create openapi directory if it doesn't exist
        openapi_dir = Path("../../openapi")
        openapi_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate JSON file
        json_file = openapi_dir / "openapi.json"
        print(f"📄 Generating {json_file}...")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(openapi_schema, f, indent=2, default=str, ensure_ascii=False)
        
        # Generate YAML file
        yaml_file = openapi_dir / "openapi.yaml"
        print(f"📄 Generating {yaml_file}...")
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(openapi_schema, f, default_flow_style=False, sort_keys=False, indent=2, allow_unicode=True)
        
        print("✅ OpenAPI documentation generated successfully!")
        print("")
        print("Generated files:")
        print(f"  📄 {json_file} - OpenAPI specification in JSON format")
        print(f"  📄 {yaml_file} - OpenAPI specification in YAML format")
        print("")
        print("To view the documentation:")
        print("  1. Start the server: poetry run uvicorn fast_api_server:app --reload --host 0.0.0.0 --port 8000")
        print("  2. Visit: http://localhost:8000/docs (Swagger UI)")
        print("  3. Visit: http://localhost:8000/redoc (ReDoc)")
        print("  4. API JSON: http://localhost:8000/openapi.json")
        print("")
        
        # Display some stats
        print("API Summary:")
        print(f"  📊 Title: {openapi_schema.get('info', {}).get('title', 'N/A')}")
        print(f"  📊 Version: {openapi_schema.get('info', {}).get('version', 'N/A')}")
        print(f"  📊 Endpoints: {len(openapi_schema.get('paths', {}))}")
        print(f"  📊 Models: {len(openapi_schema.get('components', {}).get('schemas', {}))}")
        
        # Conditionally start the server
        if start_server:
            print("\n🚀 Starting FastAPI server automatically...")
            try:
                import subprocess
                subprocess.run([sys.executable, "-m", "uvicorn", "fast_api_server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
            except KeyboardInterrupt:
                print("\n👋 Server stopped. Goodbye!")
            except Exception as e:
                print(f"\n❌ Error starting server: {e}")
        else:
            print("\n✨ OpenAPI documentation generated successfully!")
            print("💡 Tip: Start the server manually with:")
            print("   poetry run uvicorn fast_api_server:app --reload --host 0.0.0.0 --port 8000")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating OpenAPI documentation: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
