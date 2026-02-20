# AxonNexus SDK - Quick Reference

## Installation
```bash
pip install axonnexus_sdk
# or locally:
pip install -e /path/to/axonnexus_sdk
```

## Basic Usage

### Initialize Client
```python
from axonnexus_sdk import AxonNexusClient

# Production
client = AxonNexusClient(api_key="your_api_key")

# Development (no rate limit warnings)
client = AxonNexusClient(api_key="axn_test_123")
```

### Send Chat Message
```python
response = client.chat("Your question here")
response = client.chat("Your question", model="gpt-4")
```

### Make Generic Request
```python
response = client.request(
    endpoint="/endpoint",
    payload={"key": "value"},
    model="model-name",
    method="POST"  # GET, POST, PUT, DELETE
)
```

### Get Usage Stats
```python
stats = client.get_usage_stats()
# Returns: {request_count, token_usage, rate_limit_threshold, is_dev_mode}
```

### Reset Stats
```python
client.reset_usage_stats()
```

### Cleanup
```python
client.close()
# or use context manager:
with AxonNexusClient(api_key="key") as client:
    response = client.chat("message")
```

## Configuration Options

```python
client = AxonNexusClient(
    api_key="your_key",              # Required
    base_url="https://custom.url",   # Optional, defaults to HuggingFace Spaces
    timeout=30                        # Optional, seconds
)
```

## Common Patterns

### With Environment Variables
```python
import os
api_key = os.getenv("AXONNEXUS_API_KEY")
client = AxonNexusClient(api_key=api_key)
```

### Error Handling
```python
import requests

try:
    response = client.chat("message")
except ValueError as e:
    print(f"Input error: {e}")
except requests.exceptions.RequestException as e:
    print(f"API error: {e}")
```

### Batch Processing
```python
messages = ["Q1", "Q2", "Q3"]
for msg in messages:
    response = client.chat(msg)
    print(response.get("message"))

stats = client.get_usage_stats()
print(f"Tokens: {stats['token_usage']}")
```

### Rate Limit Checking
```python
stats = client.get_usage_stats()
if stats['token_usage'] > 8000:
    print("⚠️ Approaching rate limit")
```

## Response Format

Typical API response:
```json
{
    "message": "Response text",
    "model": "model-name",
    "timestamp": "2026-01-31T12:00:00",
    "usage": {
        "tokens": 150
    }
}
```

## Methods Reference

| Method | Parameters | Returns |
|--------|-----------|---------|
| `chat()` | message, model | Dict |
| `request()` | endpoint, payload, model, method | Dict |
| `get_usage_stats()` | none | Dict |
| `reset_usage_stats()` | none | None |
| `close()` | none | None |

## HTTP Methods

```python
# POST (default)
client.request(endpoint="/path", payload={...}, method="POST")

# GET
client.request(endpoint="/path", method="GET")

# PUT
client.request(endpoint="/path", payload={...}, method="PUT")

# DELETE
client.request(endpoint="/path", method="DELETE")
```

## Special Features

### Dev Mode
- Use: `api_key="axn_test_123"`
- Effect: No rate limit warnings

### Rate Limit Warnings
- Threshold: 10,000 tokens
- Automatic estimation: 1 token ≈ 4 characters
- Disabled in dev mode

### Token Tracking
- Automatic tracking of tokens used
- Manual reset with `reset_usage_stats()`
- Check with `get_usage_stats()`

## Version Info
```python
import axonnexus_sdk
print(axonnexus_sdk.__version__)  # 1.0.0
print(axonnexus_sdk.__author__)   # Atharv (Nubprogrammer)
```

## Community
- Discord: https://dsc.gg/axoninnova
- Creator: Atharv (Nubprogrammer)

## Troubleshooting

### Import Error
```
pip install -e /home/nubprogrammer/AxonNexus/axonnexus_sdk
```

### API Key Error
```
Error: Unauthorized
→ Check if API key is valid
→ Verify key has not expired
```

### Timeout Error
```
Error: Request timed out
→ Increase timeout: AxonNexusClient(api_key=key, timeout=60)
→ Check network connection
```

### Connection Error
```
Error: Failed to connect
→ Check API is running
→ Verify base_url is correct
→ Check internet connection
```

---

**Quick Links:**
- 📖 Full Docs: See README.md
- 💡 Examples: See EXAMPLES.md
- 🛠️ Installation: See INSTALL.md
- 🤝 Contributing: See CONTRIBUTING.md
