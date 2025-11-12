# Django Error Logger - Quick Reference

## 📦 Installation

```bash
pip install /Users/imoliner/prj/peercards/backend/django-error-logger/dist/django_error_logger-1.0.0-py3-none-any.whl
```

## ⚙️ Settings (settings.py)

```python
INSTALLED_APPS = [
    # ...
    'error_logger',
]

MIDDLEWARE = [
    # ...
    'error_logger.middleware.ErrorLoggingMiddleware',
]
```

## 🔗 URLs (urls.py)

```python
urlpatterns = [
    # ...
    path('error-logger/', include('error_logger.urls')),
]
```

## 🗄️ Migrate

```bash
python manage.py migrate error_logger
```

## ✅ Done!

Errors will now be automatically logged to the database.

View them at: `/admin/error_logger/errorlog/`

## 📍 Package Location

**Wheel File**: `/Users/imoliner/prj/peercards/backend/django-error-logger/dist/django_error_logger-1.0.0-py3-none-any.whl`

**Source**: `/Users/imoliner/prj/peercards/backend/django-error-logger/`

## 📖 Documentation

- `INSTALL.md` - Complete installation guide
- `README.md` - Full features and usage
- `QUICKSTART.md` - 5-step integration
- `DISTRIBUTION.md` - Distribution methods
