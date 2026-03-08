"""
Test Script for Chat API Endpoints - Phase III: Todo AI Chatbot.

This script tests the chat endpoints using HTTP requests.
Note: Requires the FastAPI server to be running.

Usage:
    1. Start server: python main.py
    2. Run tests: python test_chat_api.py
"""

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://localhost:8000"

# Get a valid JWT token from Better Auth (you'll need to replace this)
# For testing, you can get a token by logging in through the frontend
# or by inspecting the browser's localStorage/cookies
TEST_TOKEN = os.getenv("TEST_JWT_TOKEN", "")

def get_headers():
    """Get headers with authorization."""
    headers = {"Content-Type": "application/json"}
    if TEST_TOKEN:
        headers["Authorization"] = f"Bearer {TEST_TOKEN}"
    return headers


def test_create_conversation():
    """Test creating a new conversation."""
    print("\n" + "=" * 60)
    print("TEST: Create Conversation")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/conversations",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Created conversation: {data['conversation_id'][:8]}...")
            return data['conversation_id']
        else:
            print(f"[ERROR] {response.status_code}: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Is it running?")
        return None
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_send_message(conversation_id=None):
    """Test sending a message to the chat."""
    print("\n" + "=" * 60)
    print("TEST: Send Message")
    print("=" * 60)
    
    payload = {
        "message": "What tasks do I have?",
    }
    
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/",
            headers=get_headers(),
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] AI Response: {data['message']['content'][:100]}...")
            print(f"[SUCCESS] Conversation ID: {data['conversation_id'][:8]}...")
            print(f"[SUCCESS] Tool Calls: {len(data['tool_calls'])}")
            return data
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - Invalid or missing JWT token")
            print("\nTo fix this:")
            print("1. Log in through the frontend")
            print("2. Copy your JWT token from browser storage")
            print("3. Set TEST_JWT_TOKEN in .env or as environment variable")
            return None
        else:
            print(f"[ERROR] {response.status_code}: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Is it running?")
        return None
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_get_messages(conversation_id):
    """Test getting message history."""
    print("\n" + "=" * 60)
    print("TEST: Get Message History")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/chat/conversations/{conversation_id}/messages",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Retrieved {data['count']} messages")
            for msg in data['messages'][-3:]:  # Show last 3
                role = msg['role']
                content = msg['content'][:50]
                print(f"  [{role}]: {content}...")
            return data
        else:
            print(f"[ERROR] {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_list_conversations():
    """Test listing all conversations."""
    print("\n" + "=" * 60)
    print("TEST: List Conversations")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/chat/conversations",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Found {len(data)} conversations")
            for conv in data[:3]:  # Show first 3
                print(f"  - {conv['id'][:8]}... (session: {conv['session_id'][:8]}...)")
            return data
        else:
            print(f"[ERROR] {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None


def test_delete_conversation(conversation_id):
    """Test deleting a conversation."""
    print("\n" + "=" * 60)
    print("TEST: Delete Conversation")
    print("=" * 60)
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/chat/conversations/{conversation_id}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Deleted conversation: {data['deleted_conversation_id'][:8]}...")
            return True
        else:
            print(f"[ERROR] {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False


def test_unauthorized():
    """Test that endpoints reject unauthorized requests."""
    print("\n" + "=" * 60)
    print("TEST: Unauthorized Access (should fail)")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/",
            headers={"Content-Type": "application/json"},
            json={"message": "test"}
        )
        
        if response.status_code == 401:
            print(f"[SUCCESS] Correctly rejected unauthorized request")
            return True
        else:
            print(f"[ERROR] Should have returned 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False


def main():
    """Run all chat API tests."""
    print("\n" + "=" * 60)
    print("Phase III: Chat API Endpoint Tests")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    
    # Test 1: Unauthorized access
    test_unauthorized()
    
    # Check if we have a token
    if not TEST_TOKEN:
        print("\n[WARNING] No TEST_JWT_TOKEN found")
        print("\nTo run full tests:")
        print("1. Set TEST_JWT_TOKEN environment variable")
        print("2. Or add to .env: TEST_JWT_TOKEN=your-token-here")
        print("\nSkipping authenticated tests...")
        return
    
    # Test 2: Create conversation
    conversation_id = test_create_conversation()
    
    if not conversation_id:
        print("\n[ABORT] Cannot continue without conversation")
        return
    
    # Test 3: Send message
    response_data = test_send_message(conversation_id)
    
    if response_data:
        conversation_id = response_data['conversation_id']
    
    # Test 4: Get message history
    test_get_messages(conversation_id)
    
    # Test 5: List conversations
    test_list_conversations()
    
    # Test 6: Send another message
    test_send_message(conversation_id)
    
    # Test 7: Delete conversation
    test_delete_conversation(conversation_id)
    
    print("\n" + "=" * 60)
    print("Chat API Tests Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
