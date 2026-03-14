"""Test API and agent."""
import logging
logging.basicConfig(level=logging.INFO)

from ai_agents.openrouter_agent import OpenRouterAgent

agent = OpenRouterAgent('debug-user')
print(f"API Key: {agent.api_key[:20]}...")
print(f"Model: {agent.model}")
print(f"Base URL: {agent.base_url}")

# Test a simple message
result = agent.process_message("Hello")
print(f"Response: {result.content}")
