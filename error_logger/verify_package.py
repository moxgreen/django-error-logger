#!/usr/bin/env python
"""
Verification script for django-error-logger package
Run this script to verify the package is properly structured before distribution.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists and report status"""
    exists = os.path.isfile(filepath)
    status = "✓" if exists else ("✗ REQUIRED" if required else "- Optional")
    print(f"{status} {filepath}")
    return exists

def check_dir_exists(dirpath, required=True):
    """Check if a directory exists and report status"""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else ("✗ REQUIRED" if required else "- Optional")
    print(f"{status} {dirpath}/")
    return exists

def main():
    print("Django Error Logger - Package Verification")
    print("=" * 60)
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    print("\n📄 Core Files:")
    required_files = [
        '__init__.py',
        'admin.py',
        'apps.py',
        'forms.py',
        'middleware.py',
        'models.py',
        'urls.py',
        'views.py',
    ]
    
    for filename in required_files:
        filepath = script_dir / filename
        if not check_file_exists(filepath, required=True):
            return False
    
    print("\n📄 Documentation:")
    doc_files = [
        'README.md',
        'LICENSE',
        'CHANGELOG.md',
        'QUICKSTART.md',
        'DISTRIBUTION.md',
    ]
    
    for filename in doc_files:
        filepath = script_dir / filename
        check_file_exists(filepath, required=False)
    
    print("\n📄 Package Configuration:")
    config_files = [
        'setup.py',
        'pyproject.toml',
        'MANIFEST.in',
        '.gitignore',
    ]
    
    for filename in config_files:
        filepath = script_dir / filename
        if not check_file_exists(filepath, required=True):
            return False
    
    print("\n📁 Directories:")
    required_dirs = [
        'migrations',
        'templates',
        'templates/error_logger',
    ]
    
    for dirname in required_dirs:
        dirpath = script_dir / dirname
        if not check_dir_exists(dirpath, required=True):
            return False
    
    print("\n📄 Migration Files:")
    migration_files = [
        'migrations/__init__.py',
        'migrations/0001_initial.py',
    ]
    
    for filename in migration_files:
        filepath = script_dir / filename
        if not check_file_exists(filepath, required=True):
            return False
    
    print("\n📄 Template Files:")
    template_files = [
        'templates/error_logger/test_post_error.html',
        'templates/error_logger/test_large_post_error.html',
    ]
    
    for filename in template_files:
        filepath = script_dir / filename
        check_file_exists(filepath, required=False)
    
    print("\n" + "=" * 60)
    print("✅ Package verification complete!")
    print("\nNext steps:")
    print("1. Review the files listed above")
    print("2. Update version numbers in setup.py and pyproject.toml if needed")
    print("3. Build the package: python -m build")
    print("4. Install locally to test: pip install -e .")
    print("5. See DISTRIBUTION.md for distribution options")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
