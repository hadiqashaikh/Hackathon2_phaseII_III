import httpx

print("Testing POST /api/chat/message...")
response = httpx.post(
    "http://localhost:8000/api/chat/message",
    json={"message": "add task buy milk"},
    timeout=30
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
