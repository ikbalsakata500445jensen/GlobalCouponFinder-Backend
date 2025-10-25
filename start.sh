#!/bin/bash
# Start script for Railway deployment

echo "Starting GlobalCouponFinder Backend..."

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port $PORT
