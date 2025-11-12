# Django Error Logger - Installation Guide

## 📦 Installation Methods

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