import sys
import traceback
import json
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import ExceptionReporter
from .models import ErrorLog

# Maximum size for POST data logging (in bytes) - default 100KB
MAX_POST_SIZE = 100 * 1024  # 100KB

class ErrorLoggingMiddleware(MiddlewareMixin):
    # Fields to exclude from logging
    SENSITIVE_FIELDS = [
        'password', 'password1', 'password2', 'old_password', 'new_password',
        'token', 'access_token', 'refresh_token', 'api_key', 'secret',
        'credit_card', 'cvv', 'ssn', 'pin'
    ]
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.MAX_POST_SIZE = MAX_POST_SIZE
 
    def sanitize_data(self, data):
        """Remove sensitive fields from data"""
        if not isinstance(data, dict):
            return data
        
        sanitized = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in self.SENSITIVE_FIELDS):
                sanitized[key] = '***REDACTED***'
            elif isinstance(value, dict):
                sanitized[key] = self.sanitize_data(value)
            elif isinstance(value, list) and value and isinstance(value[0], str):
                # Handle Django's QueryDict which has lists of values
                sanitized[key] = value
            else:
                sanitized[key] = value
        return sanitized
    
    def process_exception(self, request, exception):
        user = request.user if request.user.is_authenticated else None
        
        # Capture full traceback (plain text)
        tb = traceback.format_exc()
        
        # Generate Django's debug HTML error page
        reporter = ExceptionReporter(request, *sys.exc_info())
        html_error = reporter.get_traceback_html()
        
        # Capture POST/PUT/PATCH data (with size limit and sanitization)
        post_data = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                # Check payload size first
                content_length = request.META.get('CONTENT_LENGTH')
                if content_length and int(content_length) > self.MAX_POST_SIZE:
                    post_data = {
                        'error': 'POST payload too large to log',
                        'size_bytes': int(content_length),
                        'size_kb': round(int(content_length) / 1024, 2),
                        'size_mb': round(int(content_length) / (1024 * 1024), 2)
                    }
                else:
                    # Payload is within size limit, proceed with logging
                    if request.content_type and 'application/json' in request.content_type:
                        body = request.body.decode('utf-8')
                        # Double-check actual body size
                        if len(body) > self.MAX_POST_SIZE:
                            post_data = {
                                'error': 'POST payload too large to log',
                                'size_bytes': len(body),
                                'size_kb': round(len(body) / 1024, 2)
                            }
                        else:
                            post_data = json.loads(body)
                    else:
                        post_data = dict(request.POST)
                        if request.FILES:
                            post_data['_files'] = {
                                k: {
                                    'name': v.name,
                                    'size': v.size,
                                    'content_type': v.content_type
                                } for k, v in request.FILES.items()
                            }
                    
                    # Sanitize sensitive data
                    if post_data and 'error' not in post_data:
                        post_data = self.sanitize_data(post_data)
                        
            except Exception as e:
                post_data = {'error': f'Could not parse POST data: {str(e)}'}
        
        # Store additional context
        additional_info = {
            'post_data': post_data,
            'request_headers': dict(request.headers),
        }
        
        ErrorLog.objects.create(
            user=user,
            error_message=str(exception),
            error_type=exception.__class__.__name__,
            traceback=tb,
            html_traceback=html_error,
            path=request.path,
            method=request.method,
            user_agent=request.META.get('HTTP_USER_AGENT'),
            ip_address=self.get_client_ip(request),
            query_string=request.META.get('QUERY_STRING', ''),
            additional_info=additional_info,
        )
        
        # Return None to let Django's default error handling continue
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip