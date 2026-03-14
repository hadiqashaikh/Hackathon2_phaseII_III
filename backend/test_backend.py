"""
Test script to verify backend is working.
"""

import httpx
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("\n" + "="*50)
    print("TEST 1: Health Check")
    print("="*50)
    
    response = httpx.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    print("✅ PASSED")
    return True


def test_root():
    """Test root endpoint."""
    print("\n" + "="*50)
    print("TEST 2: Root Endpoint")
    print("="*50)
    
    response = httpx.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    print("✅ PASSED")
    return True


def test_docs():
    """Test docs endpoint."""
    print("\n" + "="*50)
    print("TEST 3: API Docs")
    print("="*50)
    
    response = httpx.get(f"{BASE_URL}/docs")
    print(f"Status: {response.status_code}")
    
    assert response.status_code == 200
    print("✅ PASSED")
    return True


def test_chat():
    """Test chat endpoint (DEBUG mode)."""
    print("\n" + "="*50)
    print("TEST 4: AI Chat (DEBUG mode)")
    print("="*50)
    
    try:
        response = httpx.post(
            f"{BASE_URL}/api/chat/message",
            json={"message": "list my tasks"},
            timeout=30
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ PASSED")
            return True
        else:
            print(f"⚠ Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_tasks():
    """Test tasks endpoint (DEBUG mode)."""
    print("\n" + "="*50)
    print("TEST 5: Tasks API (DEBUG mode)")
    print("="*50)
    
    try:
        # List tasks
        response = httpx.get(f"{BASE_URL}/api/tasks/")
        print(f"List tasks - Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ PASSED")
            return True
        else:
            print(f"⚠ Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("TODO AI CHATBOT BACKEND - TEST SUITE")
    print("="*60)
    
    results = []
    
    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    results.append(("API Docs", test_docs()))
    results.append(("AI Chat", test_chat()))
    results.append(("Tasks API", test_tasks()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Backend is ready!")
        return 0
    else:
        print("\n⚠ Some tests failed. Check logs for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
