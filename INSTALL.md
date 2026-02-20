# AxonNexus SDK - Installation & Quick Start Guide

## 📦 Complete Directory Structure

```
/home/nubprogrammer/AxonNexus/axonnexus_sdk/
├── axonnexus_sdk/
│   ├── __init__.py          # Package initialization, exports AxonNexusClient
│   └── client.py            # Main SDK client with all methods
├── setup.py                 # PyPI configuration & metadata
├── README.md                # Full documentation with examples
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore rules
```

## 🚀 Quick Installation Steps

### Option 1: Install from Local Directory (Development)

```bash
cd /home/nubprogrammer/AxonNexus/axonnexus_sdk
pip install -e .
```

The `-e` flag installs in "editable" mode - changes to the code are reflected immediately without reinstalling.

### Option 2: Install from Directory (Normal)

```bash
cd /home/nubprogrammer/AxonNexus/axonnexus_sdk
pip install .
```

### Option 3: Install Globally (After Publishing to PyPI)

```bash
pip install axonnexus_sdk
```

## ✅ Verify Installation

```python
from axonnexus_sdk import AxonNexusClient

# Check version
import axonnexus_sdk
print(f"AxonNexus SDK version: {axonnexus_sdk.__version__}")

# Create a test client
client = AxonNexusClient(api_key="axn_test_123")
print("✓ SDK installed successfully!")
```

## 📝 Quick Test

```python
from axonnexus_sdk import AxonNexusClient

# Initialize with your API key
client = AxonNexusClient(api_key="your_actual_api_key")

# Test chat
try:
    response = client.chat("Hello AxonNexus!")
    print("Response:", response)
except Exception as e:
    print(f"Error: {e}")

# Check usage
stats = client.get_usage_stats()
print("Usage stats:", stats)
```

## 🔧 Publishing to PyPI

### Step 1: Install build tools
```bash
pip install build twine
```

### Step 2: Build the package
```bash
cd /home/nubprogrammer/AxonNexus/axonnexus_sdk
python -m build
```

This creates `dist/axonnexus_sdk-1.0.0-py3-none-any.whl` and `dist/axonnexus_sdk-1.0.0.tar.gz`

### Step 3: Upload to PyPI
```bash
python -m twine upload dist/*
```

You'll be prompted for your PyPI credentials.

### Step 4: Verify it's published
```bash
pip install axonnexus_sdk
```

## 📚 Main Features Checklist

- ✅ **Flexible API Usage** - `client.request()` accepts any endpoint
- ✅ **Easy Authentication** - Pass `api_key` to constructor
- ✅ **Dev Mode** - Use `api_key="axn_test_123"` for testing
- ✅ **Chat Method** - `client.chat(message, model="default")`
- ✅ **Generic Requests** - `client.request(endpoint, payload, method)`
- ✅ **Rate Limiting** - Automatic warnings when exceeding 10k tokens
- ✅ **Token Tracking** - `client.get_usage_stats()`
- ✅ **Context Manager** - `with AxonNexusClient(...) as client:`
- ✅ **Type Hints** - Full type annotation coverage
- ✅ **Error Handling** - Comprehensive exception handling
- ✅ **Discord Integration** - Ready for Discord bots
- ✅ **CLI Integration** - Ready for command-line tools
- ✅ **Production Ready** - Docstrings, error handling, best practices

## 🎯 Key Methods

### Basic Chat
```python
response = client.chat("Your message here", model="default")
```

### Generic Request
```python
response = client.request(
    endpoint="/custom-endpoint",
    payload={"key": "value"},
    model="model-name",
    method="POST"
)
```

### Usage Stats
```python
stats = client.get_usage_stats()
# Returns: {request_count, token_usage, rate_limit_threshold, is_dev_mode}
```

### Reset Stats
```python
client.reset_usage_stats()
```

## 🔑 Environment Setup

Create `.env` file in your project:
```
AXONNEXUS_API_KEY=your_api_key_here
```

Use in code:
```python
import os
from dotenv import load_dotenv
from axonnexus_sdk import AxonNexusClient

load_dotenv()
client = AxonNexusClient(api_key=os.getenv("AXONNEXUS_API_KEY"))
```

## 🐛 Troubleshooting

### Import Error
```
ModuleNotFoundError: No module named 'axonnexus_sdk'
```
**Solution**: Reinstall with `pip install -e .` from the package directory

### "axn_test_123" not working
**Solution**: Dev mode only works with this exact string. For production, use your real API key.

### Rate limit warning appearing
**Solution**: Use `client.get_usage_stats()` to check current usage and reset if needed.

## 📞 Support & Community

- **Discord**: https://dsc.gg/axoninnova
- **Creator**: Atharv (Nubprogrammer)
- **GitHub Issues**: Report bugs on the project repository

## 📋 Next Steps

1. ✅ SDK Structure Created
2. ✅ All Files Generated
3. ⏳ Test locally: `pip install -e .`
4. ⏳ Create GitHub repository
5. ⏳ Publish to PyPI when ready
6. ⏳ Share with community!

---

**Version**: 1.0.0  
**Author**: Atharv (Nubprogrammer)  
**License**: MIT  
**Status**: Production Ready 🚀
