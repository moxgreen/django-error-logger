# Django Error Logger

Keep It Simple and Stupid replacement of Sentry for error logging in django project.

A Django application that logs HTTP 500 errors to the database, capturing detailed context including user information, request details, and POST data.

## Features

- **Automatic Error Logging**: Captures all unhandled exceptions (HTTP 500 errors)
- **User Context**: Logs the authenticated user when the error occurred
- **Request Details**: Captures path, method, headers, IP address, and query string
- **POST Data Logging**: Saves POST/PUT/PATCH payloads with sensitive field redaction
- **Large Payload Protection**: Filters out POST payloads larger than 100KB
- **HTML Traceback**: Stores Django's debug error page HTML for detailed debugging
- **User Impersonation**: Link to impersonate the user and reproduce the error (optional)
- **Django Admin Integration**: View and manage error logs through Django admin

## Installation

### Method 1: Install from PyPI (Recommended)

From any Django project:

```bash
pip install django-error-logger
```

## 🚀 Quick Integration

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

### Step 5: Test It

```bash
# Start your Django server
python manage.py runserver

# Trigger a test error (development only!)
curl http://localhost:8000/error-logger/test/500/

# Check Django admin
open http://localhost:8000/admin/error_logger/errorlog/
```

### Step 6: User Permissions
To access the error logger views (such as the error log list, details, and test endpoints), users must be logged in and have the error_logger.view_errorlog permission. This permission is automatically created when you run migrations.

#### Assigning Permissions
You can assign this permission to users or groups via the Django admin interface:

 1. Go to the Django admin at /admin/.
 1. Navigate to **Users** or **Groups**.
 1. Select a user or group.
 1. In the permissions section, check the box for **Can view error log** under the **Error logger** app.
 1. Save the changes.

Alternatively, you can assign permissions programmatically in your code or via fixtures.

Note: Only users with this permission can access the error logger URLs. Ensure your authentication system is properly configured.


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


## ⚠️ Production Considerations

Before deploying to production:

1. **Remove Test Endpoints**: Comment out or remove test views in `error_logger/views.py`
2. **Access Control**: Ensure only admin users can access `/error-logger/` URLs
3. **Log Cleanup**: Implement a strategy to clean up old error logs
4. **Review Sensitive Fields**: Customize the `SENSITIVE_FIELDS` list for your app
5. **Database Size**: Monitor error log table size

---

## Configuration

### Sensitive Fields

The following fields are automatically redacted in POST data logs:

- `password`, `password1`, `password2`, `old_password`, `new_password`
- `token`, `access_token`, `refresh_token`, `api_key`, `secret`
- `credit_card`, `cvv`, `ssn`, `pin`

You can customize this list in `middleware.py`:

```python
SENSITIVE_FIELDS = [
    'password', 'token', 'api_key', 'secret',
    # Add your custom sensitive fields here
]
```

### POST Data Size Limit

By default, POST payloads larger than 100KB are not logged in full. You can adjust this in `middleware.py`:

```python
MAX_POST_SIZE = 100 * 1024  # 100KB (default)
# MAX_POST_SIZE = 1024 * 1024  # 1MB
```

## Usage

### Django Admin

Access the error logs through Django admin at `/admin/error_logger/errorlog/`

Features:
- List view with error type, time, user, path, and method
- Filter by error type, time, and method
- Search by error message, path, or username
- Detail view with full traceback and HTML error page
- "Open in Full Page" button to view the HTML traceback
- "Impersonate and visit error page" button (requires `django_su`)

### Test Endpoints

**⚠️ Important**: These endpoints should only be accessible in development/testing environments. Remove or restrict access in production.

Access these endpoints at `/error-logger/test/`:

#### 1. Simple 500 Error
**URL**: `/error-logger/test/500/`

Triggers a `ZeroDivisionError` to test basic error logging.

```bash
curl http://localhost:8000/error-logger/test/500/
```

#### 2. ValueError Test
**URL**: `/error-logger/test/value-error/`

Triggers a `ValueError` with a custom message.

```bash
curl http://localhost:8000/error-logger/test/value-error/
```

#### 3. KeyError Test
**URL**: `/error-logger/test/key-error/`

Triggers a `KeyError` by accessing a non-existent dictionary key.

```bash
curl http://localhost:8000/error-logger/test/key-error/
```

#### 4. POST Error Test
**URL**: `/error-logger/test/post-error/`

Tests error logging with POST data including sensitive fields (password, token).

**Form Fields**:
- `username`: Regular text field
- `password`: Will be redacted in logs
- `email`: Email field
- `token`: Will be redacted in logs

**Usage**:
1. Visit the URL in your browser
2. Fill out the form (pre-populated with test data)
3. Submit the form to trigger an error
4. Check Django admin to see POST data with sensitive fields redacted

**cURL Example**:
```bash
curl -X POST http://localhost:8000/error-logger/test/post-error/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=secret123&email=test@example.com&token=abc123"
```

#### 5. Large POST Error Test
**URL**: `/error-logger/test/large-post-error/`

Tests error logging with a large POST payload (150KB) that exceeds the logging limit.

**Form Fields**:
- `username`: Regular text field
- `password`: Will be redacted in logs
- `large_field`: Pre-filled with 150KB of data

**Usage**:
1. Visit the URL in your browser
2. Submit the form (large_field is pre-populated)
3. Check Django admin to see that POST data size is logged but content is not

**Expected Result**: 
The error log's `additional_info` should contain:
```json
{
  "post_data": {
    "error": "POST payload too large to log",
    "size_bytes": 153600,
    "size_kb": 150.0,
    "size_mb": 0.15
  }
}
```

## Model Structure

### ErrorLog Model

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | User who encountered the error (null if anonymous) |
| `error_message` | TextField | Plain text exception message |
| `error_type` | CharField | Exception class name (e.g., "ValueError") |
| `traceback` | TextField | Plain text Python traceback |
| `html_traceback` | TextField | HTML version of Django's debug page |
| `error_time` | DateTimeField | When the error occurred |
| `path` | CharField | Request path |
| `method` | CharField | HTTP method (GET, POST, etc.) |
| `user_agent` | CharField | User's browser/client |
| `ip_address` | GenericIPAddressField | Client IP address |
| `query_string` | TextField | URL query parameters |
| `additional_info` | JSONField | POST data and request headers |

## Security Considerations

1. **Sensitive Data**: Always review the `SENSITIVE_FIELDS` list to ensure all sensitive data in your application is redacted
2. **Access Control**: Error logs contain sensitive information. Ensure only authorized users (admin group) can access them
3. **Test Endpoints**: Remove or restrict access to test endpoints in production
4. **Database Storage**: Error logs can accumulate. Implement a cleanup strategy (e.g., delete logs older than 90 days)
5. **HTML Traceback**: Contains full request context. Ensure admin access is properly secured



## Requirements

- Django 3.2+
- Python 3.8+
- `django_su` (for user impersonation feature)

## License

AGPL-3.0