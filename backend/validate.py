"""
Simple test script to validate the backend functionality.
This script is not a comprehensive test suite but can be used
for basic validation of the backend during development.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

def test_api_docs():
    """Test if API documentation is accessible."""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"API Docs Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error accessing API docs: {e}")
        return False

def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Health Check Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error accessing health check: {e}")
        return False

if __name__ == "__main__":
    print("Validating backend endpoints...")

    print("\nTesting API Documentation...")
    docs_ok = test_api_docs()

    print("\nTesting Health Check...")
    health_ok = test_health_check()

    print(f"\nValidation Summary:")
    print(f"API Docs accessible: {docs_ok}")
    print(f"Health Check works: {health_ok}")

    if docs_ok and health_ok:
        print("Basic validation passed! The backend appears to be running correctly.")
    else:
        print("Validation failed. Please check if the backend is running on http://localhost:8000")