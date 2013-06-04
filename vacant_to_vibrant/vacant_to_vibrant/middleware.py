try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


class MonitorMiddleware(object):
    """
    Patched version of django-monitor's MonitorMiddleware that sets
    monitor_user to None when the user is not authenticated (eg,
    AnonymousUser).
    """
    def process_request(self, request):
        user = getattr(request, 'user', None)
        if user and not user.is_authenticated():
            user = None
        _thread_locals.monitor_user = user
