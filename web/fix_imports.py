#!/usr/bin/env python3
"""
Fix import issues - Run this if you get import errors
"""
import sys
from pathlib import Path

# Add web directory to Python path
web_dir = Path(__file__).parent
sys.path.insert(0, str(web_dir))

print("✓ Python path configured")
print(f"  Web directory: {web_dir}")

# Test imports
print("\nTesting imports...")

try:
    from config import get_config
    print("✓ config.py")
except ImportError as e:
    print(f"✗ config.py: {e}")

try:
    from models import db, User, Organization
    print("✓ models")
except ImportError as e:
    print(f"✗ models: {e}")

try:
    from utils.jwt_utils import create_access_token
    print("✓ utils.jwt_utils")
except ImportError as e:
    print(f"✗ utils.jwt_utils: {e}")

try:
    from services.auth_service import AuthService
    print("✓ services.auth_service")
except ImportError as e:
    print(f"✗ services.auth_service: {e}")

try:
    from api import api
    print("✓ api")
except ImportError as e:
    print(f"✗ api: {e}")

print("\n" + "="*50)
print("If all imports show ✓, you're good to go!")
print("If any show ✗, check the error message above")
print("="*50 + "\n")
