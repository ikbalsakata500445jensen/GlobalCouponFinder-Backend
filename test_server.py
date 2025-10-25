#!/usr/bin/env python3
"""
Simple test script to start the FastAPI server
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    from main import app
    print("✓ FastAPI app imported successfully!")
    
    print("Testing server startup...")
    import uvicorn
    print("✓ Uvicorn imported successfully!")
    
    print("Starting server on http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
