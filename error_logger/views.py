from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ErrorLog
from .forms import TestPostErrorForm, TestLargePostForm
import json

def is_admin(user):
    """Check if user belongs to the 'admin' group"""
    return user.groups.filter(name='admin').exists()

def can_read_errorlog(user):
    """Check if user has permission to view ErrorLog"""
    return user.has_perm('error_logger.view_errorlog')

def errorlog_reader_required(view_func):
    """Decorator to restrict access to users who can read ErrorLog"""
    decorated_view = login_required(user_passes_test(can_read_errorlog)(view_func))
    return decorated_view

@errorlog_reader_required
def error_log_list(request):
    logs = ErrorLog.objects.all().order_by('-error_time')
    return render(request, 'error_logger/error_log_list.html', {'logs': logs})

@errorlog_reader_required
def error_log_detail(request, log_id):
    log = ErrorLog.objects.get(id=log_id)
    return render(request, 'error_logger/error_log_detail.html', {'log': log})

@errorlog_reader_required
def error_log_html(request, log_id):
    """Display the full HTML traceback page"""
    log = get_object_or_404(ErrorLog, id=log_id)
    return HttpResponse(log.html_traceback)

@errorlog_reader_required
def test_500_error(request):
    """
    Test view to trigger a 500 error for testing the error logger.
    """
    # This will raise a ZeroDivisionError
    result = 1 / 0
    return HttpResponse("This should never be reached")

@errorlog_reader_required
def test_value_error(request):
    """
    Test view to trigger a ValueError.
    """
    raise ValueError("This is a test ValueError for error logging")

@errorlog_reader_required
def test_key_error(request):
    """
    Test view to trigger a KeyError.
    """
    test_dict = {'key': 'value'}
    return HttpResponse(test_dict['nonexistent_key'])

@errorlog_reader_required
def test_post_error(request):
    """
    Test view to trigger an error with POST data.
    """
    if request.method == 'POST':
        form = TestPostErrorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # Trigger an error
            raise ValueError(f"Test POST error - username: {username}")
    else:
        form = TestPostErrorForm()
    
    return render(request, 'error_logger/test_post_error.html', {'form': form})

@errorlog_reader_required
def test_large_post_error(request):
    """
    Test view to trigger an error with large POST data.
    """
    if request.method == 'POST':
        form = TestLargePostForm(request.POST)
        # Trigger error regardless of form validity
        raise ValueError("Test error with large POST payload")
    else:
        form = TestLargePostForm()
    
    return render(request, 'error_logger/test_large_post_error.html', {'form': form})