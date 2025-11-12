# Django Error Logger - Quick Start Guide

## Installation in 5 Steps

### 1. Copy the App

Copy the `error_logger` directory to your Django project:

```bash
cp -r /path/to/peercards/backend/error_logger /path/to/your-project/
```

### 2. Update Settings

Add to `settings.py`:

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ... your other middleware ...
    'error_logger.middleware.ErrorLoggingMiddleware',  # Add this at the end
]
```

### 3. Update URLs

Add to your main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... your other URLs ...
    path('error-logger/', include('error_logger.urls')),  # Add this
]
```

### 4. Run Migrations

```bash
python manage.py migrate error_logger
```

### 5. Test It

Visit a test endpoint (development only):

```bash
curl http://localhost:8000/error-logger/test/500/
```

Then check Django admin at: `http://localhost:8000/admin/error_logger/errorlog/`

## That's It!

The error logger is now active and will automatically capture all 500 errors in your Django application.

## Optional: User Impersonation

If you want the "impersonate user" feature in the admin:

```bash
pip install django-su
```

Add to `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_su',
    'error_logger',
]
```

Add to `urls.py`:

```python
urlpatterns = [
    # ...
    path('su/', include('django_su.urls')),
]
```

## Production Checklist

Before deploying to production:

- [ ] Remove or restrict access to test endpoints in `error_logger/views.py`
- [ ] Ensure only admin users can access `/error-logger/` URLs
- [ ] Set up a cleanup strategy for old error logs
- [ ] Review and customize `SENSITIVE_FIELDS` in middleware
- [ ] Test that sensitive data is properly redacted

## Next Steps

- Read the full [README.md](README.md) for detailed features
- See [DISTRIBUTION.md](DISTRIBUTION.md) for packaging options
- Customize sensitive fields and POST size limits as needed
