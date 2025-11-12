# Django Error Logger - Installation Guide

## ✅ Package Ready!

Your `django-error-logger` package has been successfully built and is ready for distribution!

**Package Location**: `/Users/imoliner/prj/peercards/backend/django-error-logger/dist/`

Built files:
- `django_error_logger-1.0.0-py3-none-any.whl` (17KB) - Wheel format (recommended)
- `django_error_logger-1.0.0.tar.gz` (13KB) - Source distribution

---

## 📦 Installation Methods

### Method 1: Install from Local Wheel (Recommended)

From any Django project:

```bash
pip install /Users/imoliner/prj/peercards/backend/django-error-logger/dist/django_error_logger-1.0.0-py3-none-any.whl
```

Or if you copy the wheel file to your project:

```bash
pip install django_error_logger-1.0.0-py3-none-any.whl
```

### Method 2: Install from Source Distribution

```bash
pip install /Users/imoliner/prj/peercards/backend/django-error-logger/dist/django_error_logger-1.0.0.tar.gz
```

### Method 3: Install in Development Mode

For active development, install in editable mode:

```bash
cd /Users/imoliner/prj/peercards/backend/django-error-logger
pip install -e .
```

This creates a link to the source code, so changes are immediately reflected.

### Method 4: Add to requirements.txt

```txt
# Local installation
django-error-logger @ file:///Users/imoliner/prj/peercards/backend/django-error-logger/dist/django_error_logger-1.0.0-py3-none-any.whl

# Or from a shared location
django-error-logger @ file:///path/to/shared/django_error_logger-1.0.0-py3-none-any.whl
```

Then install:

```bash
pip install -r requirements.txt
```

### Method 5: Install from Git (if pushed to a repo)

Once pushed to GitHub/GitLab:

```bash
# From GitHub
pip install git+https://github.com/yourusername/django-error-logger.git

# From GitLab  
pip install git+https://gitlab.com/yourusername/django-error-logger.git

# From a specific branch
pip install git+https://github.com/yourusername/django-error-logger.git@main

# From a specific tag
pip install git+https://github.com/yourusername/django-error-logger.git@v1.0.0
```

### Method 6: Upload to PyPI (Public)

To make it publicly available on PyPI:

```bash
# Install twine (already installed)
pip install twine

# Upload to Test PyPI first (recommended)
twine upload --repository testpypi dist/*

# Then anyone can install with:
pip install --index-url https://test.pypi.org/simple/ django-error-logger

# Upload to production PyPI
twine upload dist/*

# Then anyone can install with:
pip install django-error-logger
```

### Method 7: Private Package Server

For internal company use, upload to:
- AWS CodeArtifact
- Google Artifact Registry
- Azure Artifacts
- JFrog Artifactory
- Gemfury

---

## 🚀 Quick Integration (5 Steps)

After installation, integrate into your Django project:

### Step 1: Add to INSTALLED_APPS

Edit `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ... your other apps ...
    'error_logger',  # Add this
]
```

### Step 2: Add Middleware

Edit `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ... your other middleware ...
    'error_logger.middleware.ErrorLoggingMiddleware',  # Add at the end
]
```

### Step 3: Add URLs

Edit your main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... your other URLs ...
    path('error-logger/', include('error_logger.urls')),  # Add this
]
```

### Step 4: Run Migrations

```bash
python manage.py migrate error_logger
```

### Step 5: Test It!

```bash
# Start your Django server
python manage.py runserver

# Trigger a test error (development only!)
curl http://localhost:8000/error-logger/test/500/

# Check Django admin
open http://localhost:8000/admin/error_logger/errorlog/
```

---

## 📋 Verification Checklist

After installation, verify everything works:

```bash
# Check if package is installed
pip show django-error-logger

# Verify imports work
python -c "import error_logger; print('✓ Package imported successfully')"

# Check Django can find the app
python manage.py check

# Verify migrations
python manage.py showmigrations error_logger

# Run migrations
python manage.py migrate error_logger
```

Expected output:
```
✓ Package imported successfully
System check identified no issues (0 silenced).
error_logger
 [X] 0001_initial
```

---

## 🔧 Optional: User Impersonation Feature

To enable the "impersonate user" feature in admin:

```bash
pip install django-su
```

Then add to `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_su',
    'error_logger',
]
```

And add to `urls.py`:

```python
urlpatterns = [
    # ...
    path('su/', include('django_su.urls')),
]
```

---

## 🔄 Updating the Package

When you make changes and want to redistribute:

### Step 1: Update Version

Edit `setup.py` and `pyproject.toml`:

```python
version="1.1.0"  # Increment version
```

### Step 2: Rebuild

```bash
cd /Users/imoliner/prj/peercards/backend/django-error-logger

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Rebuild
python -m build
```

### Step 3: Reinstall in Projects

In projects using the package:

```bash
# Uninstall old version
pip uninstall django-error-logger

# Install new version
pip install /path/to/django_error_logger-1.1.0-py3-none-any.whl
```

---

## 📤 Distribution Options

### Option A: Share the Wheel File

Simply copy the `.whl` file to a shared location:

```bash
# Copy to shared network drive
cp dist/django_error_logger-1.0.0-py3-none-any.whl /shared/packages/

# Others can install with:
pip install /shared/packages/django_error_logger-1.0.0-py3-none-any.whl
```

### Option B: Set Up a Simple Package Server

```bash
# Install pypiserver
pip install pypiserver

# Create a packages directory
mkdir ~/pypi-packages
cp dist/*.whl ~/pypi-packages/

# Start the server
pypi-server run -p 8080 ~/pypi-packages/

# Others can install with:
pip install --index-url http://your-server:8080/simple/ django-error-logger
```

### Option C: Use Git Repository

```bash
# Push to Git
cd /Users/imoliner/prj/peercards/backend/django-error-logger
git init
git add .
git commit -m "Initial release of django-error-logger v1.0.0"
git tag v1.0.0
git remote add origin https://github.com/yourusername/django-error-logger.git
git push -u origin main
git push --tags

# Others can install with:
pip install git+https://github.com/yourusername/django-error-logger.git
```

---

## 🧪 Testing the Installation

Create a test Django project to verify:

```bash
# Create test project
django-admin startproject testproject
cd testproject

# Install your package
pip install /Users/imoliner/prj/peercards/backend/django-error-logger/dist/django_error_logger-1.0.0-py3-none-any.whl

# Follow the 5 integration steps above

# Test error logging
python manage.py runserver
# Visit: http://localhost:8000/error-logger/test/500/
# Check: http://localhost:8000/admin/error_logger/errorlog/
```

---

## ⚠️ Production Considerations

Before deploying to production:

1. **Remove Test Endpoints**: Comment out or remove test views in `error_logger/views.py`
2. **Access Control**: Ensure only admin users can access `/error-logger/` URLs
3. **Log Cleanup**: Implement a strategy to clean up old error logs
4. **Review Sensitive Fields**: Customize the `SENSITIVE_FIELDS` list for your app
5. **Database Size**: Monitor error log table size

---

## 📚 Next Steps

- **Read**: `README.md` for complete documentation
- **Quick Reference**: `QUICKSTART.md` for integration steps  
- **Customization**: `DISTRIBUTION.md` for advanced topics
- **Support**: Check `error_logger/views.py` for test examples

---

## 🎉 Success!

You now have a standard pip package that can be:
✅ Installed with `pip install`  
✅ Added to `requirements.txt`  
✅ Distributed to other projects  
✅ Uploaded to PyPI  
✅ Installed from Git repositories  

**Installation command**:
```bash
pip install /Users/imoliner/prj/peercards/backend/django-error-logger/dist/django_error_logger-1.0.0-py3-none-any.whl
```
