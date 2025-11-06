from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = ['admin', 'zookeeper']

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect('login')
            # if profile missing, deny
            profile = getattr(user, 'profile', None)
            if profile is None:
                raise PermissionDenied
            if profile.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
