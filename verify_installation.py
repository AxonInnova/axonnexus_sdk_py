#!/usr/bin/env python3
"""
AxonNexus SDK - Quick Start Verification Script

This script verifies that the AxonNexus SDK is correctly installed
and ready to use.

Run this script after installing the SDK to verify everything works.
"""

import sys
import os

def verify_installation():
    """Verify the SDK installation"""
    
    print("\n" + "=" * 70)
    print("AxonNexus SDK - Installation Verification")
    print("=" * 70 + "\n")
    
    # Step 1: Import check
    print("[1/5] Checking imports...")
    try:
        from axonnexus_sdk import (
            AxonNexusClient,
            AxonNexusError,
            AuthenticationError,
            RateLimitError,
            QuotaExceededError,
            APIError,
        )
        print("      ✓ All imports successful")
    except ImportError as e:
        print(f"      ✗ Import failed: {e}")
        return False
    
    # Step 2: Version check
    print("\n[2/5] Checking version...")
    try:
        import axonnexus_sdk
        version = axonnexus_sdk.__version__
        print(f"      ✓ Version: {version}")
    except Exception as e:
        print(f"      ✗ Version check failed: {e}")
        return False
    
    # Step 3: Client creation
    print("\n[3/5] Creating client...")
    try:
        client = AxonNexusClient(api_key="axn_test_123")
        print(f"      ✓ Client created successfully")
        print(f"      ✓ Base URL: {client.base_url}")
        print(f"      ✓ Dev mode: {client.is_dev_mode}")
    except Exception as e:
        print(f"      ✗ Client creation failed: {e}")
        return False
    
    # Step 4: Feature verification
    print("\n[4/5] Verifying features...")
    try:
        stats = client.get_usage_stats()
        print(f"      ✓ Usage tracking: {list(stats.keys())}")
        
        client.reset_usage_stats()
        print(f"      ✓ Stats reset works")
        
        repr_str = repr(client)
        print(f"      ✓ String representation: {repr_str}")
        
        client.close()
        print(f"      ✓ Client cleanup works")
    except Exception as e:
        print(f"      ✗ Feature check failed: {e}")
        return False
    
    # Step 5: Context manager verification
    print("\n[5/5] Verifying context manager...")
    try:
        with AxonNexusClient(api_key="axn_test_123") as ctx_client:
            pass
        print(f"      ✓ Context manager works")
    except Exception as e:
        print(f"      ✗ Context manager failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ SDK Installation Verified Successfully!")
    print("=" * 70)
    
    print("\n📖 Next Steps:")
    print("   1. Read the README.md for full documentation")
    print("   2. Check EXAMPLES.md for practical examples")
    print("   3. Use QUICKREF.md for quick reference")
    print("\n🚀 Quick Start:")
    print("   from axonnexus_sdk import AxonNexusClient")
    print("   client = AxonNexusClient(api_key='your-api-key')")
    print("   response = client.chat('Hello!')")
    print("   print(response)")
    print("\n")
    
    return True

if __name__ == "__main__":
    success = verify_installation()
    sys.exit(0 if success else 1)
