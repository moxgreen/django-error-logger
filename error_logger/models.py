from django.db import models
from django.contrib.auth.models import User

class ErrorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    error_message = models.TextField()  # Plain text - str(exception)
    error_type = models.CharField(max_length=255)  # e.g., "ValueError", "ZeroDivisionError"
    traceback = models.TextField()  # Plain text - full Python traceback
    html_traceback = models.TextField(blank=True, null=True)  # HTML version of Django's debug page
    error_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=500)  # Request path
    method = models.CharField(max_length=10)  # GET, POST, etc.
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    query_string = models.TextField(blank=True)  # URL query parameters
    additional_info = models.JSONField(blank=True, null=True)  # For any extra context

    class Meta:
        ordering = ['-error_time']
        
    def __str__(self):
        return f"{self.error_type} at {self.error_time} by {self.user if self.user else 'Anonymous'}"