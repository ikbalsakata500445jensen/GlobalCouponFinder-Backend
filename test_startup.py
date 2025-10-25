#!/usr/bin/env python3
"""
Simple test to verify the backend can start without database issues
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import app
    print("✅ FastAPI app imported successfully")
    
    # Test if we can get the health endpoint
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    # Test health endpoint
    response = client.get("/health")
    print(f"✅ Health endpoint: {response.status_code} - {response.json()}")
    
    # Test root endpoint
    response = client.get("/")
    print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
    
    print("🎉 Backend startup test PASSED!")
    
except Exception as e:
    print(f"❌ Backend startup test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
