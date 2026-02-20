# Contributing to AxonNexus SDK

Thank you for your interest in contributing to the AxonNexus SDK! This guide will help you get started.

## Code of Conduct

Be respectful, inclusive, and supportive of other contributors. Harassment or discrimination of any kind is not tolerated.

## Getting Started

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/axonnexus_sdk.git
cd axonnexus_sdk
pip install -e .
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Follow the existing code style
- Add type hints to all functions
- Write comprehensive docstrings
- Add examples in docstrings

### 4. Test Your Changes
```bash
python -m pytest tests/
# or test manually:
python -c "from axonnexus_sdk import AxonNexusClient; client = AxonNexusClient(api_key='axn_test_123'); print('OK')"
```

### 5. Update Documentation
- Update README.md if adding new features
- Add examples to EXAMPLES.md
- Update docstrings

### 6. Submit a Pull Request
- Provide a clear description of changes
- Reference any related issues
- Keep commits clean and descriptive

## Code Style

### Type Hints
Always use type hints:
```python
def chat(self, message: str, model: str = "default") -> Dict[str, Any]:
    """Send a chat message."""
    pass
```

### Docstrings
Use Google-style docstrings:
```python
def example_function(param1: str, param2: int) -> bool:
    """
    Short description of what the function does.
    
    Longer description if needed.
    
    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2.
        
    Returns:
        bool: Description of return value.
        
    Raises:
        ValueError: When something is invalid.
        
    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    """
```

### Naming Conventions
- Use snake_case for functions and variables
- Use PascalCase for classes
- Use UPPER_CASE for constants
- Private methods start with underscore

## Adding a New Feature

### Example: Adding a new method

1. Add method to `axonnexus_sdk/client.py`:
```python
def new_feature(self, param: str) -> Dict[str, Any]:
    """
    Brief description.
    
    Args:
        param (str): Description.
        
    Returns:
        dict: Description.
        
    Example:
        >>> client = AxonNexusClient(api_key="key")
        >>> result = client.new_feature("value")
    """
    payload = {"param": param}
    return self._make_request("POST", "/new-endpoint", payload)
```

2. Add to exports in `axonnexus_sdk/__init__.py` if needed

3. Add example to `EXAMPLES.md`:
```python
# Example: Using new_feature
response = client.new_feature("value")
print(response)
```

4. Update `README.md` with usage documentation

## Testing Guidelines

### Unit Tests
Create `tests/test_client.py`:
```python
import pytest
from axonnexus_sdk import AxonNexusClient

def test_initialization():
    client = AxonNexusClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.is_dev_mode is False

def test_dev_mode():
    client = AxonNexusClient(api_key="axn_test_123")
    assert client.is_dev_mode is True

def test_invalid_api_key():
    with pytest.raises(ValueError):
        AxonNexusClient(api_key="")
```

### Manual Testing
```bash
# Test basic functionality
python -c "
from axonnexus_sdk import AxonNexusClient
client = AxonNexusClient(api_key='axn_test_123')
stats = client.get_usage_stats()
print('✓ Stats:', stats)
"
```

## Documentation Guidelines

### README.md Updates
- Keep examples clear and concise
- Include output examples
- Update table of contents if adding sections

### EXAMPLES.md Updates
- Include comments explaining what code does
- Show common pitfalls
- Demonstrate error handling
- Show both simple and advanced usage

### Docstrings
- Describe what, not how
- Include examples in docstrings
- Document exceptions that can be raised
- Use present tense

## Version Management

The SDK uses semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

Update version in:
- `setup.py`
- `axonnexus_sdk/__init__.py`
- `README.md` (changelog section)

## Release Checklist

- [ ] All tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Version bumped
- [ ] Changelog updated
- [ ] No uncommitted changes
- [ ] Tests run on multiple Python versions (3.8, 3.9, 3.10, 3.11)

## Reporting Issues

When reporting a bug, include:
- Python version
- SDK version
- Minimal code to reproduce
- Expected vs actual behavior
- Error messages and traceback

## Feature Requests

When requesting a feature:
- Describe the use case
- Provide examples
- Explain why it's needed
- Link to related issues if any

## Community

- **Discord**: https://dsc.gg/axoninnova
- **Discussion**: Use GitHub Discussions for questions
- **Issues**: Use GitHub Issues for bugs and features

## License

By contributing, you agree your code will be licensed under MIT License.

---

Thank you for contributing to AxonNexus SDK! 🚀
