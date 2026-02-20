# AxonNexus SDK - Practical Examples

This file contains real-world usage examples for the AxonNexus SDK.

## Example 1: Simple Chat Application

```python
from axonnexus_sdk import AxonNexusClient

def main():
    # Initialize client
    client = AxonNexusClient(api_key="your_api_key")
    
    # Interactive chat loop
    print("AxonNexus Chat (type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        try:
            response = client.chat(user_input)
            print(f"Bot: {response.get('message', 'No response')}\n")
        except Exception as e:
            print(f"Error: {e}\n")
    
    # Show final stats
    stats = client.get_usage_stats()
    print(f"\nSession Stats:")
    print(f"  - Requests: {stats['request_count']}")
    print(f"  - Tokens Used: {stats['token_usage']}")
    
    client.close()

if __name__ == "__main__":
    main()
```

## Example 2: Discord Bot Integration

```python
import discord
from discord.ext import commands
import os
from axonnexus_sdk import AxonNexusClient

# Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize AxonNexus client
axn_client = AxonNexusClient(api_key=os.getenv("AXONNEXUS_API_KEY"))

@bot.event
async def on_ready():
    print(f"✓ Bot logged in as {bot.user}")

@bot.command(name="ask")
async def ask_axonnexus(ctx, *, question: str):
    """Ask AxonNexus anything"""
    async with ctx.typing():
        try:
            response = axn_client.chat(question)
            answer = response.get("message", "No response")
            
            # Split if too long (Discord 2000 char limit)
            if len(answer) > 2000:
                answer = answer[:1997] + "..."
            
            embed = discord.Embed(
                title="AxonNexus Response",
                description=answer,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Model: {response.get('model', 'unknown')}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name="stats")
async def show_stats(ctx):
    """Show API usage statistics"""
    stats = axn_client.get_usage_stats()
    embed = discord.Embed(
        title="AxonNexus Usage Stats",
        color=discord.Color.green()
    )
    embed.add_field(name="Requests", value=stats['request_count'])
    embed.add_field(name="Tokens Used", value=stats['token_usage'])
    embed.add_field(name="Limit", value=stats['rate_limit_threshold'])
    embed.add_field(name="Dev Mode", value=stats['is_dev_mode'])
    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
```

## Example 3: CLI Tool

```python
#!/usr/bin/env python3
"""
AxonNexus CLI Tool
Usage: python axn_cli.py "Your question here"
"""

import sys
import os
from axonnexus_sdk import AxonNexusClient

def main():
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python axn_cli.py <message>")
        print("Example: python axn_cli.py 'What is Python?'")
        sys.exit(1)
    
    message = " ".join(sys.argv[1:])
    
    # Get API key from environment
    api_key = os.getenv("AXONNEXUS_API_KEY")
    if not api_key:
        print("Error: AXONNEXUS_API_KEY environment variable not set")
        sys.exit(1)
    
    # Make request
    try:
        with AxonNexusClient(api_key=api_key, timeout=60) as client:
            print(f"🤖 Question: {message}")
            response = client.chat(message)
            print(f"✓ Answer: {response.get('message', 'No response')}")
            print(f"📊 Model: {response.get('model', 'unknown')}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Example 4: Batch Processing with Usage Tracking

```python
from axonnexus_sdk import AxonNexusClient

def process_batch(api_key, questions):
    """Process multiple questions and track usage"""
    
    client = AxonNexusClient(api_key=api_key)
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"Processing {i}/{len(questions)}: {question[:50]}...")
        
        try:
            response = client.chat(question)
            results.append({
                'question': question,
                'answer': response.get('message'),
                'model': response.get('model'),
                'success': True
            })
        except Exception as e:
            results.append({
                'question': question,
                'error': str(e),
                'success': False
            })
        
        # Check if approaching rate limit
        stats = client.get_usage_stats()
        if stats['token_usage'] > 8000:
            print("⚠️  Warning: Approaching rate limit!")
    
    # Summary
    print("\n" + "="*50)
    print("BATCH PROCESSING SUMMARY")
    print("="*50)
    print(f"Total processed: {len(questions)}")
    print(f"Successful: {sum(1 for r in results if r['success'])}")
    print(f"Failed: {sum(1 for r in results if not r['success'])}")
    
    stats = client.get_usage_stats()
    print(f"\nUsage Statistics:")
    print(f"  - Total Requests: {stats['request_count']}")
    print(f"  - Total Tokens: {stats['token_usage']}")
    print(f"  - Limit: {stats['rate_limit_threshold']}")
    
    return results

# Example usage
if __name__ == "__main__":
    questions = [
        "What is machine learning?",
        "Explain neural networks",
        "How does deep learning work?",
        "What is computer vision?",
    ]
    
    results = process_batch("your_api_key", questions)
    
    # Print results
    for result in results:
        if result['success']:
            print(f"\n✓ Q: {result['question']}")
            print(f"  A: {result['answer'][:100]}...")
        else:
            print(f"\n✗ Q: {result['question']}")
            print(f"  Error: {result['error']}")
```

## Example 5: Custom Endpoint Usage

```python
from axonnexus_sdk import AxonNexusClient

def main():
    client = AxonNexusClient(api_key="your_api_key")
    
    # Example 1: Image generation endpoint (hypothetical)
    image_response = client.request(
        endpoint="/generate-image",
        payload={
            "prompt": "a beautiful sunset over mountains",
            "size": "512x512",
            "style": "oil painting"
        },
        model="image-gen-v1"
    )
    print("Generated image:", image_response)
    
    # Example 2: Text analysis endpoint
    analysis_response = client.request(
        endpoint="/analyze",
        payload={
            "text": "The quick brown fox jumps over the lazy dog.",
            "analysis_type": "sentiment"
        },
        model="analyzer-v2"
    )
    print("Analysis result:", analysis_response)
    
    # Example 3: Translation endpoint
    translation_response = client.request(
        endpoint="/translate",
        payload={
            "text": "Hello, how are you?",
            "source_lang": "en",
            "target_lang": "es"
        },
        model="translator-v1"
    )
    print("Translation:", translation_response)
    
    client.close()

if __name__ == "__main__":
    main()
```

## Example 6: Error Handling Best Practices

```python
from axonnexus_sdk import AxonNexusClient
import requests
import time

def robust_chat_with_retry(api_key, message, max_retries=3):
    """Chat with retry logic and error handling"""
    
    client = AxonNexusClient(api_key=api_key, timeout=30)
    
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat(message)
            return response
        
        except ValueError as e:
            print(f"❌ Input error: {e}")
            return None
        
        except requests.exceptions.Timeout:
            print(f"⏱️  Timeout (attempt {attempt}/{max_retries})")
            if attempt < max_retries:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        
        except requests.exceptions.ConnectionError as e:
            print(f"🔌 Connection error: {e}")
            if attempt < max_retries:
                print(f"Retrying in 5 seconds...")
                time.sleep(5)
        
        except requests.exceptions.RequestException as e:
            print(f"❌ API error: {e}")
            return None
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    print(f"Failed after {max_retries} attempts")
    return None

# Usage
if __name__ == "__main__":
    response = robust_chat_with_retry(
        "your_api_key",
        "Tell me about Python programming"
    )
    if response:
        print("Success:", response.get('message'))
```

## Example 7: Context Manager Usage

```python
from axonnexus_sdk import AxonNexusClient

def demo_context_manager():
    """Demonstrates proper resource cleanup with context manager"""
    
    # Automatic cleanup when exiting the with block
    with AxonNexusClient(api_key="your_api_key") as client:
        # Make multiple requests
        response1 = client.chat("First question")
        print("Response 1:", response1)
        
        response2 = client.chat("Second question")
        print("Response 2:", response2)
        
        # Get stats before cleanup
        stats = client.get_usage_stats()
        print("\nFinal Stats:")
        print(f"  Requests: {stats['request_count']}")
        print(f"  Tokens: {stats['token_usage']}")
    
    # Session is automatically closed here
    print("✓ Session cleaned up automatically")

if __name__ == "__main__":
    demo_context_manager()
```

## Example 8: Development vs Production

```python
from axonnexus_sdk import AxonNexusClient
import os

def main():
    # Development mode - no rate limit warnings
    if os.getenv("ENVIRONMENT") == "development":
        client = AxonNexusClient(api_key="axn_test_123")
        print("🧪 Running in development mode (no rate limits)")
    else:
        # Production mode
        api_key = os.getenv("AXONNEXUS_API_KEY")
        if not api_key:
            raise ValueError("AXONNEXUS_API_KEY not set in production")
        client = AxonNexusClient(api_key=api_key)
        print("🚀 Running in production mode (rate limits active)")
    
    # Use client
    response = client.chat("Hello!")
    print(response)
    
    client.close()

if __name__ == "__main__":
    main()
```

---

## Tips for Production Use

1. **Always use environment variables** for API keys
2. **Implement retry logic** for network failures
3. **Monitor usage stats** regularly
4. **Use context managers** for automatic cleanup
5. **Handle all exception types** appropriately
6. **Log important events** for debugging
7. **Test with dev mode** before production
8. **Cache responses** when possible to save tokens

---

For more examples and community support, visit: https://dsc.gg/axoninnova
