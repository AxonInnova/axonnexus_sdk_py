"""
AxonNexus SDK - Production-ready Python SDK for the AxonNexus API.

This SDK provides a simple, flexible interface to interact with the AxonNexus API
hosted on Hugging Face Spaces.

Example:
    >>> from axonnexus_sdk import AxonNexusClient
    >>> client = AxonNexusClient(api_key="your-api-key")
    >>> response = client.chat(message="Hello!")
    >>> print(response)
    >>> client.close()

Or with context manager:
    >>> with AxonNexusClient(api_key="your-api-key") as client:
    ...     response = client.chat(message="Hello!")
"""

from .client import (
    AxonNexusClient,
    AxonNexusError,
    AuthenticationError,
    RateLimitError,
    QuotaExceededError,
    APIError,
)

__version__ = "1.0.0"
__author__ = "Atharv (AxonNexus)"
__license__ = "MIT"

__all__ = [
    "AxonNexusClient",
    "AxonNexusError",
    "AuthenticationError",
    "RateLimitError",
    "QuotaExceededError",
    "APIError",
]
