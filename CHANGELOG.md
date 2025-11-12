# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-11

### Added
- Initial release of Django Error Logger
- Automatic HTTP 500 error logging to database
- User context capture (authenticated user tracking)
- Request details logging (path, method, headers, IP, query string)
- POST/PUT/PATCH data logging with sensitive field redaction
- Large payload protection (100KB limit)
- HTML traceback storage (Django debug page)
- Django admin integration with list and detail views
- Optional user impersonation feature (requires django-su)
- Test endpoints for development/testing
- Customizable sensitive fields list
- Configurable POST data size limits

### Features
- **ErrorLog Model**: Comprehensive error tracking with timestamps
- **Middleware**: ErrorLoggingMiddleware for automatic error capture
- **Admin Interface**: Full-featured admin with HTML traceback viewing
- **Security**: Automatic redaction of passwords, tokens, API keys, etc.
- **Performance**: Payload size limits to prevent database bloat
- **Developer-Friendly**: Test endpoints and detailed tracebacks

### Dependencies
- Django >= 3.2
- Python >= 3.8
- django-su >= 1.0.0 (optional, for impersonation feature)

### Documentation
- Comprehensive README.md with usage examples
- Distribution guide (DISTRIBUTION.md)
- Quick start guide (QUICKSTART.md)
- Setup.py and pyproject.toml for packaging
- AGPL-3.0 License

### Security
- Sensitive field redaction in POST data
- Admin-only access to error logs
- IP address tracking for security auditing
- Optional user impersonation with proper authentication

## [Unreleased]

### Planned
- Management command for cleaning up old error logs
- Email notifications for critical errors
- Slack/Discord webhook integration
- Error rate limiting
- Grouped error views (same error type/message)
- Error statistics dashboard
