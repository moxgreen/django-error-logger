# Django Error Logger - Distribution Guide

This guide explains how to package and distribute the error_logger app to be used in other Django projects.

## Package Structure

The error_logger app has been configured as a standalone, redistributable Django package with the following structure:

```
error_logger/
├── __init__.py
├── admin.py                    # Django admin configuration
├── apps.py                     # App configuration
├── forms.py                    # Test forms
├── middleware.py               # Error logging middleware
├── models.py                   # ErrorLog model
├── urls.py                     # URL configuration
├── views.py                    # Views including test endpoints
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
├── templates/
│   └── error_logger/
│       ├── test_large_post_error.html
│       └── test_post_error.html
├── README.md                   # Documentation
├── LICENSE                     # MIT License
├── setup.py                    # Setup configuration (legacy)
├── pyproject.toml             # Modern Python packaging
├── MANIFEST.in                # Package data inclusion
└── .gitignore                 # Git ignore file
```

## Distribution Methods

### Method 1: Copy to Another Project (Simplest)

1. Copy the entire `error_logger` directory to your Django project
2. Follow the installation instructions in README.md
3. Run migrations

```bash
# Example
cp -r /path/to/peercards/backend/error_logger /path/to/your-project/
cd /path/to/your-project
python manage.py migrate error_logger
```

### Method 2: Install as Python Package (Local)

You can install the package locally in editable mode for development:

```bash
cd error_logger
pip install -e .
```

Or install normally:

```bash
pip install /path/to/error_logger
```

### Method 3: Create Distribution Package

Build a distributable wheel/tarball:

```bash
cd error_logger

# Install build tools
pip install build

# Build the package
python -m build

# This creates:
# - dist/django-error-logger-1.0.0.tar.gz
# - dist/django_error_logger-1.0.0-py3-none-any.whl
```

Then install from the built package:

```bash
pip install dist/django_error_logger-1.0.0-py3-none-any.whl
```

### Method 4: Install from Git Repository

If you push this to a Git repository:

```bash
# Install from GitHub
pip install git+https://github.com/yourusername/django-error-logger.git

# Install specific branch
pip install git+https://github.com/yourusername/django-error-logger.git@main

# Install specific tag/version
pip install git+https://github.com/yourusername/django-error-logger.git@v1.0.0
```

Add to requirements.txt:

```
# From GitHub
django-error-logger @ git+https://github.com/yourusername/django-error-logger.git

# Or from local path
-e /path/to/error_logger
```

### Method 5: Publish to PyPI (Public)

To make it available on PyPI:

```bash
# Install twine
pip install twine

# Build the package
python -m build

# Upload to Test PyPI first (recommended)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

Then anyone can install with:

```bash
pip install django-error-logger
```

### Method 6: Private Package Repository

For private/internal use, host on a private PyPI server or use alternatives like:

- **AWS CodeArtifact**
- **Google Artifact Registry**
- **JFrog Artifactory**
- **Azure Artifacts**
- **Gemfury**

## Dependencies

The package has minimal dependencies:

- **Required**: Django >= 3.2
- **Optional**: django-su >= 1.0.0 (for user impersonation feature)

Install with optional dependencies:

```bash
pip install django-error-logger[impersonation]
```

## Configuration After Installation

Regardless of installation method, you need to:

1. Add to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    # ...
    'error_logger',
]
```

2. Add middleware:

```python
MIDDLEWARE = [
    # ... other middleware ...
    'error_logger.middleware.ErrorLoggingMiddleware',
]
```

3. Include URLs:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('error-logger/', include('error_logger.urls')),
]
```

4. Run migrations:

```bash
python manage.py migrate error_logger
```

## Customization

### Sensitive Fields

Create a custom middleware that inherits from ErrorLoggingMiddleware:

```python
# myapp/middleware.py
from error_logger.middleware import ErrorLoggingMiddleware

class CustomErrorLoggingMiddleware(ErrorLoggingMiddleware):
    SENSITIVE_FIELDS = [
        'password', 'token', 'api_key', 'secret',
        'credit_card_number',  # Add your custom fields
        'social_security_number',
    ]
```

Then use your custom middleware in settings:

```python
MIDDLEWARE = [
    # ...
    'myapp.middleware.CustomErrorLoggingMiddleware',
]
```

### POST Size Limit

```python
from error_logger.middleware import ErrorLoggingMiddleware

class CustomErrorLoggingMiddleware(ErrorLoggingMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.MAX_POST_SIZE = 1024 * 1024  # 1MB
```

## Testing the Package

After installation, verify it works:

```bash
# Run Django checks
python manage.py check

# Test migrations
python manage.py migrate error_logger --dry-run

# Access test endpoints (development only!)
curl http://localhost:8000/error-logger/test/500/
```

## Security Notes

1. **Remove Test Endpoints in Production**: The test views should be restricted or removed in production environments
2. **Access Control**: Ensure only admin users can access error logs
3. **Database Cleanup**: Implement regular cleanup of old error logs
4. **Review Sensitive Fields**: Customize the SENSITIVE_FIELDS list for your application

## Maintenance

### Updating the Package

1. Make changes to the code
2. Update version in `setup.py` and `pyproject.toml`
3. Update CHANGELOG if you maintain one
4. Rebuild and redistribute

```bash
# Update version
# Edit setup.py: version="1.1.0"
# Edit pyproject.toml: version = "1.1.0"

# Rebuild
python -m build

# Redistribute using your chosen method
```

## Troubleshooting

### Import Errors

If you get import errors after installation:

```python
# Verify installation
pip show django-error-logger

# Check if it's in INSTALLED_APPS
python manage.py shell
>>> from django.conf import settings
>>> 'error_logger' in settings.INSTALLED_APPS
True
```

### Migrations Not Found

```bash
# Verify migrations are included
python manage.py showmigrations error_logger

# Force migration discovery
python manage.py makemigrations error_logger
python manage.py migrate error_logger
```

### Static Files Not Found

```bash
# Collect static files
python manage.py collectstatic
```

## Support

For issues, feature requests, or contributions, please visit:
- GitHub: https://github.com/yourusername/django-error-logger
- Documentation: See README.md

## License

MIT License - See LICENSE file for details
