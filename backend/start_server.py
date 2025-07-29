#!/usr/bin/env python3
"""
Start script for meTTaFlights Backend API
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Add the project copy directory to Python path for flight search functionality
project_copy_dir = current_dir.parent / "project copy"
sys.path.insert(0, str(project_copy_dir))

def main():
    """Start the FastAPI server"""
    try:
        print("🚀 Starting meTTaFlights Backend API...")
        print("📍 Server will be available at: http://localhost:8000")
        print("📚 API documentation will be available at: http://localhost:8000/docs")
        print("🔧 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the server
        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()