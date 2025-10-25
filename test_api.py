#!/usr/bin/env python3
"""
Test script for GlobalCouponFinder API endpoints
"""
import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing GlobalCouponFinder API...")
    print("=" * 50)
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test 2: Health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 3: Stores endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/stores")
        print(f"✅ Stores endpoint: {response.status_code}")
        data = response.json()
        print(f"   Total stores: {data.get('total', 0)}")
        print(f"   Stores returned: {len(data.get('stores', []))}")
    except Exception as e:
        print(f"❌ Stores endpoint failed: {e}")
    
    # Test 4: Stores with filters
    try:
        response = requests.get(f"{base_url}/api/v1/stores?region=america&store_type=food_delivery")
        print(f"✅ America food delivery stores: {response.status_code}")
        data = response.json()
        print(f"   America food delivery stores: {data.get('total', 0)}")
    except Exception as e:
        print(f"❌ America food delivery stores failed: {e}")
    
    # Test 5: Countries endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/stores/countries")
        print(f"✅ Countries endpoint: {response.status_code}")
        data = response.json()
        print(f"   Total countries: {len(data.get('countries', []))}")
    except Exception as e:
        print(f"❌ Countries endpoint failed: {e}")
    
    # Test 6: Region stats
    try:
        response = requests.get(f"{base_url}/api/v1/stores/regions/stats")
        print(f"✅ Region stats: {response.status_code}")
        data = response.json()
        print(f"   Stats: {data.get('stats', {})}")
    except Exception as e:
        print(f"❌ Region stats failed: {e}")
    
    print("=" * 50)
    print("API testing complete!")

if __name__ == "__main__":
    test_api()
