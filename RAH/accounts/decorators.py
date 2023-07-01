from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings



def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('user_login'))
            
        user_type = request.user.user_type

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if user_type != 'AD':
            messages.error(
                request, 'You are not allowed to access this page')
            return redirect(reverse('branch_dashboard'))

        return view_func(request, *args, **kwargs)
    return wrapper