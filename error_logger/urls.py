from django.urls import path
from . import views

app_name = 'error_logger'

urlpatterns = [
    path('logs/', views.error_log_list, name='error_log_list'),
    path('logs/<int:log_id>/', views.error_log_detail, name='error_log_detail'),
    path('logs/<int:log_id>/html/', views.error_log_html, name='error_log_html'),
    
    # Test endpoints - for testing only, remove in production
    path('test/500/', views.test_500_error, name='test_500_error'),
    path('test/value-error/', views.test_value_error, name='test_value_error'),
    path('test/key-error/', views.test_key_error, name='test_key_error'),
    path('test/post-error/', views.test_post_error, name='test_post_error'),
    path('test/large-post-error/', views.test_large_post_error, name='test_large_post_error'),
]