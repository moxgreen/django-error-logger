from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.conf import settings
from .models import ErrorLog

# Check if django_su is installed
try:
    import django_su
    DJANGO_SU_INSTALLED = True
except ImportError:
    DJANGO_SU_INSTALLED = False

@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ['error_type', 'formatted_error_time', 'user', 'path', 'method']
    list_filter = ['error_type', 'error_time', 'method']
    search_fields = ['error_message', 'path', 'user__username']
    
    def get_readonly_fields(self, request, obj=None):
        """Dynamically include impersonate_link only if django_su is installed"""
        fields = ['user', 'error_message', 'error_type', 'traceback', 
                  'html_traceback_display', 'formatted_error_time', 'path', 'method', 
                  'user_agent', 'ip_address', 'query_string']
        if DJANGO_SU_INSTALLED:
            fields.append('impersonate_link')
        return fields
    
    exclude = ['html_traceback', 'error_time']
    
    def formatted_error_time(self, obj):
        """Display error time with hours, minutes, and seconds"""
        return obj.error_time.strftime('%Y-%m-%d %H:%M:%S')
    
    formatted_error_time.short_description = "Error Time"
    formatted_error_time.admin_order_field = 'error_time'
    
    def impersonate_link(self, obj):
        """Generate link to impersonate user and visit error path (requires django_su)"""
        if not DJANGO_SU_INSTALLED:
            return format_html(
                '<span style="color: #999;">Install django-su to enable user impersonation</span>'
            )
        
        if obj.user:
            try:
                # Build the impersonation URL - django_su uses the username in the path
                su_url = reverse('su_login')
                full_url = f"{su_url}?next={obj.path}"
                if obj.query_string:
                    full_url = f"{su_url}?next={obj.path}?{obj.query_string}"
                
                return format_html(
                    '<a href="/su/{}{}?next={}" target="_blank" class="button">Impersonate {} and visit error page</a>',
                    obj.user.pk,
                    '/',
                    obj.path + ('?' + obj.query_string if obj.query_string else ''),
                    obj.user.username
                )
            except Exception as e:
                return format_html(
                    '<span style="color: #c00;">Error generating impersonation link: {}</span>',
                    str(e)
                )
        return "No user (anonymous request)"
    
    impersonate_link.short_description = "Reproduce Error"
    
    def html_traceback_display(self, obj):
        if obj.html_traceback:
            full_page_url = reverse('error_logger:error_log_html', args=[obj.id])
            return format_html(
                '<p><a href="{}" target="_blank" class="button">Open in Full Page</a></p>'
                '<iframe srcdoc="{}" style="width:100%; height:600px; border:1px solid #ccc;"></iframe>', 
                full_page_url,
                obj.html_traceback.replace('"', '&quot;')
            )
        return "No HTML traceback available"
    
    html_traceback_display.short_description = "HTML Error Page"