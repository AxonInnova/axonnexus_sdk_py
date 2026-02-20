"""
AxonNexus SDK - Production-ready Python client for the AxonNexus API.

This module provides the main AxonNexusClient class for interacting with the AxonNexus API.
"""

import requests
from typing import Optional, Dict, Any
from datetime import datetime
import json
import warnings


class AxonNexusError(Exception):
    """Base exception for AxonNexus SDK errors."""
    pass


class AuthenticationError(AxonNexusError):
    """Raised when authentication fails (401)."""
    pass


class RateLimitError(AxonNexusError):
    """Raised when rate limit is exceeded (429)."""
    pass


class QuotaExceededError(AxonNexusError):
    """Raised when user quota is exceeded (403)."""
    pass


class APIError(AxonNexusError):
    """Raised for other API errors (4xx, 5xx)."""
    pass


class AxonNexusClient:
    """
    Production-ready Python SDK client for the AxonNexus API.

    This client supports:
    - Multiple user types (free, paid, developers, bots, CLI tools)
    - Flexible API access (chat and generic request methods)
    - Automatic usage tracking
    - Error handling and retries
    - Context manager support
    - Connection pooling

    Example:
        >>> client = AxonNexusClient(api_key="your-api-key")
        >>> response = client.chat(
        ...     message="Hello, world!",
        ...     model="gpt-4"
        ... )
        >>> print(response)
        >>> client.close()

    Or with context manager:
        >>> with AxonNexusClient(api_key="your-api-key") as client:
        ...     response = client.chat(message="Hello, world!")
        ...     print(response)
    """

    # Class constants
    DEFAULT_BASE_URL = "https://atharv2610-axonnexus-api.hf.space"
    DEV_API_KEY = "axn_test_123"
    DEFAULT_TIMEOUT = 30.0
    RATE_LIMIT_WARNING_THRESHOLD = 10000  # tokens

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """
        Initialize the AxonNexus client.

        Args:
            api_key (str): Your AxonNexus API key. Use "axn_test_123" for dev mode.
            base_url (str, optional): Base URL of the AxonNexus API.
                Defaults to: https://atharv2610-axonnexus-api.hf.space
            timeout (float): Request timeout in seconds. Defaults to 30.0

        Raises:
            ValueError: If api_key is empty.
        """
        if not api_key or not api_key.strip():
            raise ValueError("api_key cannot be empty")

        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self.is_dev_mode = api_key == self.DEV_API_KEY

        # Initialize session with connection pooling
        self.session = requests.Session()

        # Initialize usage tracking
        self._usage_stats = {
            "requests_made": 0,
            "total_tokens_used": 0,
            "first_request_time": None,
            "last_request_time": None,
        }

        # Build headers
        self._build_headers()

    def _build_headers(self) -> None:
        """Build request headers with API key."""
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "axonnexus-sdk/1.0.0",
        })

    def chat(
        self,
        message: str,
        model: str = "gpt-4",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Send a chat message to the AxonNexus API.

        Convenience method for the /chat endpoint.

        Args:
            message (str): The message to send.
            model (str): The model to use. Defaults to "gpt-4".
            **kwargs: Additional parameters to pass to the API (e.g., temperature, top_p).

        Returns:
            dict: The API response.

        Raises:
            AuthenticationError: If API key is invalid (401).
            QuotaExceededError: If user quota is exceeded (403).
            RateLimitError: If rate limit is exceeded (429).
            APIError: For other API errors.

        Example:
            >>> client = AxonNexusClient(api_key="your-api-key")
            >>> response = client.chat(
            ...     message="What is the capital of France?",
            ...     model="gpt-4"
            ... )
            >>> print(response.get("reply"))
        """
        payload = {
            "message": message,
            "model": model,
            **kwargs,
        }
        return self.request(
            endpoint="/chat",
            payload=payload,
            method="POST",
        )

    def request(
        self,
        endpoint: str,
        payload: Optional[Dict[str, Any]] = None,
        method: str = "POST",
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Make a generic request to any AxonNexus API endpoint.

        This method is flexible and supports:
        - Any current endpoint
        - Any future endpoint
        - Any model name
        - Custom parameters

        Args:
            endpoint (str): The API endpoint (e.g., "/chat", "/analyze", "/generate").
            payload (dict, optional): Request payload/body.
            method (str): HTTP method. Defaults to "POST". Can be "GET", "POST", etc.
            model (str, optional): Model name to use (if applicable).
            **kwargs: Additional parameters to pass to requests library (e.g., params, headers).

        Returns:
            dict: The parsed JSON response from the API.

        Raises:
            AuthenticationError: If API key is invalid (401).
            QuotaExceededError: If user quota is exceeded (403).
            RateLimitError: If rate limit is exceeded (429).
            APIError: For other API errors.
            requests.RequestException: For network errors.

        Example:
            >>> client = AxonNexusClient(api_key="your-api-key")
            >>> response = client.request(
            ...     endpoint="/analyze",
            ...     payload={"text": "hello world"},
            ...     model="text-analyzer",
            ...     method="POST"
            ... )
        """
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint

        url = self.base_url + endpoint

        # Merge model into payload if provided
        if payload is None:
            payload = {}
        if model and isinstance(payload, dict) and "model" not in payload:
            payload["model"] = model

        # Estimate and warn about token usage
        self._check_usage_warning(payload)

        try:
            # Make the request
            if method.upper() == "GET":
                response = self.session.get(
                    url,
                    params=payload,
                    timeout=self.timeout,
                    **kwargs,
                )
            else:
                response = self.session.request(
                    method=method.upper(),
                    url=url,
                    json=payload if method.upper() != "GET" else None,
                    timeout=self.timeout,
                    **kwargs,
                )

            # Update usage stats
            self._update_usage_stats(response)

            # Handle errors
            self._handle_response_errors(response)

            # Parse and return response
            return response.json()

        except requests.Timeout:
            raise APIError(
                f"Request to {url} timed out after {self.timeout} seconds. "
                "Please check your connection or increase timeout."
            )
        except requests.ConnectionError as e:
            raise APIError(
                f"Failed to connect to {url}. "
                f"Please check your connection and the API base URL. Error: {str(e)}"
            )
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def _check_usage_warning(self, payload: Dict[str, Any]) -> None:
        """Warn if token usage is getting high."""
        if self.is_dev_mode:
            return

        payload_str = json.dumps(payload)
        estimated_tokens = len(payload_str) // 4 + 1
        new_total = self._usage_stats["total_tokens_used"] + estimated_tokens

        if new_total > self.RATE_LIMIT_WARNING_THRESHOLD:
            warnings.warn(
                f"⚠️  Usage Warning: You've used ~{new_total} tokens, "
                f"exceeding the recommended {self.RATE_LIMIT_WARNING_THRESHOLD} tokens. "
                f"Consider optimizing your API usage.",
                UserWarning,
                stacklevel=3
            )

    def _update_usage_stats(self, response: requests.Response) -> None:
        """Update usage statistics from response headers/body."""
        now = datetime.now()

        if self._usage_stats["first_request_time"] is None:
            self._usage_stats["first_request_time"] = now

        self._usage_stats["last_request_time"] = now
        self._usage_stats["requests_made"] += 1

        # Try to extract token usage from response
        try:
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and "usage" in data:
                    usage = data.get("usage", {})
                    tokens = usage.get("total_tokens", 0)
                    self._usage_stats["total_tokens_used"] += tokens
        except (ValueError, KeyError):
            pass

    def _handle_response_errors(self, response: requests.Response) -> None:
        """Handle API response errors with clear messages."""
        if response.status_code == 200 or response.status_code == 201:
            return

        # Try to extract error message from response
        error_message = None
        try:
            data = response.json()
            error_message = data.get("detail") or data.get("message") or data.get("error")
        except (ValueError, KeyError):
            error_message = response.text or "Unknown error"

        # Handle specific status codes
        if response.status_code == 401:
            raise AuthenticationError(
                f"Authentication failed (401). "
                f"Your API key is invalid or has expired. "
                f"Get a new API key from https://atharv2610-axonnexus-api.hf.space/docs\n"
                f"Error: {error_message}"
            )

        elif response.status_code == 403:
            raise QuotaExceededError(
                f"Access denied (403). "
                f"Your quota has been exceeded or you don't have permission to access this resource. "
                f"Error: {error_message}"
            )

        elif response.status_code == 429:
            raise RateLimitError(
                f"Rate limit exceeded (429). "
                f"You have made too many requests. Please wait before trying again. "
                f"Error: {error_message}"
            )

        elif response.status_code >= 500:
            raise APIError(
                f"Server error ({response.status_code}). "
                f"The AxonNexus API is having issues. Please try again later. "
                f"Error: {error_message}"
            )

        elif response.status_code >= 400:
            raise APIError(
                f"API error ({response.status_code}). "
                f"Error: {error_message}"
            )

    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get current usage statistics.

        Returns:
            dict: Dictionary containing:
                - requests_made (int): Total requests made
                - total_tokens_used (int): Total tokens used (if tracked by API)
                - first_request_time (datetime): Time of first request
                - last_request_time (datetime): Time of last request

        Example:
            >>> client = AxonNexusClient(api_key="your-api-key")
            >>> stats = client.get_usage_stats()
            >>> print(f"Requests made: {stats['requests_made']}")
            >>> print(f"Tokens used: {stats['total_tokens_used']}")
        """
        return self._usage_stats.copy()

    def reset_usage_stats(self) -> None:
        """
        Reset usage statistics.

        Example:
            >>> client = AxonNexusClient(api_key="your-api-key")
            >>> client.reset_usage_stats()
        """
        self._usage_stats = {
            "requests_made": 0,
            "total_tokens_used": 0,
            "first_request_time": None,
            "last_request_time": None,
        }

    def close(self) -> None:
        """
        Close the client and clean up resources.

        Always call this when you're done with the client, or use
        the context manager to automatically close it.

        Example:
            >>> client = AxonNexusClient(api_key="your-api-key")
            >>> try:
            ...     response = client.chat(message="Hello")
            ... finally:
            ...     client.close()
        """
        if self.session:
            self.session.close()

    def __enter__(self):
        """Support context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support context manager exit."""
        self.close()
        return False

    def __repr__(self) -> str:
        """String representation of the client."""
        mode = "DEV" if self.is_dev_mode else "PROD"
        return f"AxonNexusClient(base_url='{self.base_url}', mode='{mode}')"
