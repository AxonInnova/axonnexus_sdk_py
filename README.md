# AxonNexus SDK

A flexible, production-ready Python SDK for the AxonNexus API hosted on Hugging Face Spaces.

## Features

✨ **Flexible API Usage** - Call any endpoint or model without SDK updates  
🔐 **Easy Authentication** - Simple API key-based authentication  
⚠️ **Rate Limiting** - Automatic token usage warnings  
🚀 **Production Ready** - Type hints, docstrings, error handling  
🔌 **Discord/CLI Compatible** - Works with any Python application  
📦 **PyPI Ready** - Install via pip in seconds  

## Installation

```bash
pip install axonnexus_sdk
```

## Quick Start

### Basic Chat

```python
from axonnexus_sdk import AxonNexusClient

# Initialize the client
client = AxonNexusClient(api_key="your_api_key_here")

# Send a chat message
response = client.chat("What is machine learning?")
print(response)
```

### Using a Specific Model

```python
# Use a specific model
response = client.chat("Hello!", model="gpt-4")
print(response["message"])
```

### Generic API Requests

```python
# Make a generic request to any endpoint
response = client.request(
    endpoint="/analyze",
    payload={"text": "Sample text to analyze"},
    model="analyzer-v1"
)
print(response)
```

### Track Usage Statistics

```python
# Get usage statistics
stats = client.get_usage_stats()
print(f"Requests made: {stats['request_count']}")
print(f"Tokens used: {stats['token_usage']}")
```

### Using as Context Manager

```python
# Automatically close the connection
with AxonNexusClient(api_key="your_api_key") as client:
    response = client.chat("Hello world!")
    print(response)
# Session is automatically closed
```

## Development Mode

For testing without rate limit warnings:

```python
# Use the test API key
client = AxonNexusClient(api_key="axn_test_123")
response = client.chat("Test message")
# No rate limit warnings will be shown in dev mode
```

## Advanced Usage

### Custom Base URL

```python
# Point to a custom API endpoint
client = AxonNexusClient(
    api_key="your_api_key",
    base_url="https://custom-axonnexus-domain.com/api"
)
```

### Request Timeout

```python
# Set custom timeout (in seconds)
client = AxonNexusClient(
    api_key="your_api_key",
    timeout=60
)
```

### Making Different HTTP Methods

```python
# POST request (default)
response = client.request(
    endpoint="/process",
    payload={"data": "value"},
    method="POST"
)

# GET request
response = client.request(
    endpoint="/status",
    method="GET"
)

# PUT request
response = client.request(
    endpoint="/update",
    payload={"id": 1, "status": "active"},
    method="PUT"
)

# DELETE request
response = client.request(
    endpoint="/delete/123",
    method="DELETE"
)
```

### Reset Usage Tracking

```python
# Reset usage statistics
client.reset_usage_stats()
stats = client.get_usage_stats()
print(stats)  # All counts reset to 0
```

## Discord Bot Integration

Here's an example of using the SDK in a Discord bot:

```python
import discord
from discord.ext import commands
from axonnexus_sdk import AxonNexusClient

# Initialize bot and SDK client
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
axn_client = AxonNexusClient(api_key="your_api_key")

@bot.command(name="ask")
async def ask_axonnexus(ctx, *, message):
    """Ask AxonNexus a question"""
    try:
        # Send typing indicator
        async with ctx.typing():
            # Make the API request
            response = axn_client.chat(message)
            
            # Format and send response
            reply = response.get("message", "No response received")
            
            # Discord has a 2000 character limit
            if len(reply) > 2000:
                reply = reply[:1997] + "..."
            
            await ctx.send(reply)
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

bot.run("your_discord_token")
```

## CLI Tool Integration

Create a simple CLI tool:

```python
#!/usr/bin/env python3
"""Simple CLI tool using AxonNexus SDK"""

import sys
from axonnexus_sdk import AxonNexusClient

def main():
    if len(sys.argv) < 2:
        print("Usage: axonnexus <message>")
        sys.exit(1)
    
    message = " ".join(sys.argv[1:])
    
    # Load API key from environment
    import os
    api_key = os.getenv("AXONNEXUS_API_KEY")
    if not api_key:
        print("Error: AXONNEXUS_API_KEY not set")
        sys.exit(1)
    
    # Make request
    with AxonNexusClient(api_key=api_key) as client:
        try:
            response = client.chat(message)
            print(response.get("message", "No response"))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
```

## Adding New Endpoints or Models

The SDK is designed to be future-proof. When AxonNexus adds new endpoints or models, you don't need to update the SDK:

### Example: New Endpoint Added to AxonNexus

```python
# Even if AxonNexus adds "/generate-image" endpoint, it works immediately:
response = client.request(
    endpoint="/generate-image",
    payload={"prompt": "a beautiful sunset"},
    model="image-gen-v1"
)
```

### Example: New Model Added

```python
# Just pass the new model name:
response = client.chat("Hello", model="new-powerful-model-v2")
```

No SDK update required!

## Error Handling

```python
from axonnexus_sdk import AxonNexusClient
import requests

client = AxonNexusClient(api_key="your_api_key")

try:
    response = client.chat("Hello")
except ValueError as e:
    # Invalid input
    print(f"Input error: {e}")
except requests.exceptions.RequestException as e:
    # Network or API error
    print(f"API error: {e}")
except Exception as e:
    # Unexpected error
    print(f"Unexpected error: {e}")
```

## Configuration

### Environment Variables (Optional)

```bash
# Set your API key
export AXONNEXUS_API_KEY="your_api_key"

# Then in your code:
import os
client = AxonNexusClient(api_key=os.getenv("AXONNEXUS_API_KEY"))
```

### Rate Limiting

The SDK tracks token usage and warns when exceeding 10,000 tokens per session:

```python
client = AxonNexusClient(api_key="your_api_key")

# Check if approaching limit
stats = client.get_usage_stats()
if stats['token_usage'] > 8000:
    print("⚠️ Approaching rate limit!")
```

## API Response Format

Typical API responses follow this structure:

```json
{
    "message": "Response from the model",
    "model": "model-name",
    "timestamp": "2026-01-30T12:00:00",
    "usage": {
        "tokens": 150
    }
}
```

## Testing

```python
# Test with development mode (no rate limit warnings)
test_client = AxonNexusClient(api_key="axn_test_123")

# Make test requests
response = test_client.chat("Test message")
print(response)
```

## Troubleshooting

### "Connection refused" error
- Check if the API is running on Hugging Face Spaces
- Verify the base_url is correct
- Check your internet connection

### "Unauthorized" error
- Verify your API key is correct
- Check if the key has expired

### Timeout errors
- Increase the timeout parameter
- Check your network speed
- Try again later if the API is slow

## API Key Management

**Never hardcode API keys in your source code!** Use environment variables:

```python
import os
from axonnexus_sdk import AxonNexusClient

api_key = os.getenv("AXONNEXUS_API_KEY")
if not api_key:
    raise ValueError("AXONNEXUS_API_KEY environment variable not set")

client = AxonNexusClient(api_key=api_key)
```

## Performance Tips

1. **Reuse the client** - Don't create a new client for each request
2. **Use context manager** - Automatically handles cleanup
3. **Batch requests** - Group multiple operations together
4. **Monitor usage** - Check stats regularly to avoid rate limits

```python
# Good practice
with AxonNexusClient(api_key=api_key) as client:
    response1 = client.chat("Question 1")
    response2 = client.chat("Question 2")
    response3 = client.request("/analyze", {"text": "data"})
    
    stats = client.get_usage_stats()
    print(f"Total requests: {stats['request_count']}")
```

## Community & Support

Join our Discord community to get help, share ideas, and stay updated:

- 💬 **Discord Community**: [https://dsc.gg/axoninnova](https://dsc.gg/axoninnova)
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/yourusername/axonnexus_sdk/issues)
- 💡 **Discussions**: [GitHub Discussions](https://github.com/yourusername/axonnexus_sdk/discussions)

## About AxonNexus

**AxonNexus** is a cutting-edge platform for building and deploying AI models with ease.

**Creator/Founder**: [Atharv (Nubprogrammer)](https://github.com/Nubprogrammer)

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Changelog

### Version 1.0.0 (2026-01-31)
- Initial release
- Chat functionality
- Generic request method
- Rate limiting and usage tracking
- Full documentation
- Discord bot examples
- CLI integration examples
- Context manager support

## Roadmap

- [ ] Async/await support
- [ ] Streaming responses
- [ ] Built-in caching
- [ ] Retry logic with exponential backoff
- [ ] WebSocket support for real-time interactions
- [ ] SDK plugins system
- [ ] Type stubs for better IDE support

---

Made with ❤️ by the AxonNexus team
