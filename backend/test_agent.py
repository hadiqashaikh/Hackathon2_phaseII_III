"""
Test Script for OpenAI Agent Runner - Phase III: Todo AI Chatbot.

This script tests the OpenAI Agent integration with MCP tools.
Note: Requires a valid OPENAI_API_KEY in .env file for full API testing.

Usage:
    python test_agent.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Phase III: OpenAI Agent Initialization Test")
print("=" * 60)

from ai_agents.todo_agent import create_todo_agent, TodoAgentRunner, AGENT_NAME, AGENT_MODEL
from ai_agents.instructions import SYSTEM_INSTRUCTIONS

# Test 1: Agent Creation
print("\n[TEST 1] Creating Todo AI Agent...")
agent = create_todo_agent()
print(f"[SUCCESS] Agent created: {agent.name}")
print(f"[SUCCESS] Tools bound: {len(agent.tools)}")

print("\n--- Agent Configuration ---")
print(f"  Name: {agent.name}")
print(f"  Model: {agent.model}")
print(f"  Instructions: {len(agent.instructions)} characters")
print(f"  Tools: {[t.name for t in agent.tools]}")

# Test 2: Runner Initialization
print("\n[TEST 2] Initializing Agent Runner...")

# Get a valid user ID from database
from sqlmodel import Session, text
from database import engine

with Session(engine) as session:
    result = session.exec(text('SELECT id FROM "user" LIMIT 1'))
    user_id = result.first()

if not user_id:
    print("[ERROR] No user found in database.")
    exit(1)

user_id_str = user_id[0] if isinstance(user_id, tuple) else user_id
runner = TodoAgentRunner(user_id=user_id_str)
print(f"[SUCCESS] Agent runner initialized for user: {user_id_str[:8]}...")

# Test 3: Check API Key
print("\n[TEST 3] Checking OpenAI API Key...")
api_key = os.getenv("OPENAI_API_KEY", "")
if not api_key or "placeholder" in api_key or "sk-place" in api_key:
    print("[WARNING] Placeholder API key detected")
    print("\nTo test full agent functionality:")
    print("1. Get an OpenAI API key from https://platform.openai.com/api-keys")
    print("2. Add it to backend/.env: OPENAI_API_KEY=sk-your-key-here")
    print("3. Run: python test_agent.py")
else:
    print(f"[SUCCESS] API key found: {api_key[:8]}...")
    
    # Test 4: Full Agent Test (only with valid API key)
    print("\n[TEST 4] Testing Agent Message Processing...")
    
    try:
        response = runner.process_message_sync("What tasks do I have?")
        print(f"[SUCCESS] Agent Response: {response.content[:100]}...")
        print(f"[SUCCESS] Tool Calls: {len(response.tool_calls)}")
    except Exception as e:
        print(f"[ERROR] Agent test failed: {str(e)[:100]}")

print("\n" + "=" * 60)
print("Agent Initialization Test Complete!")
print("=" * 60)
