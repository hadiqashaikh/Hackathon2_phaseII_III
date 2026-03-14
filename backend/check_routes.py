import httpx
import json

response = httpx.get("http://localhost:8000/openapi.json")
openapi = response.json()

print("Registered routes with /api/chat:")
for path in sorted(openapi.get('paths', {}).keys()):
    if '/api/chat' in path or '/chat' in path:
        methods = list(openapi['paths'][path].keys())
        print(f"  {path} - {methods}")
