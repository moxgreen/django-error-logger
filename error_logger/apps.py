from django.apps import AppConfig

class ErrorLoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'error_logger'
    verbose_name = 'Error Logger'