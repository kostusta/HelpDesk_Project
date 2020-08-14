import datetime
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import redirect, render

SESSION_TIMEOUT = settings.SESSION_IDLE_TIMEOUT


class AutoLogoutUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            current_datetime = datetime.datetime.now()
            if 'last_active_time' in request.session:
                active_period = (current_datetime - request.session.get('last_active_time')).seconds
                if active_period > SESSION_TIMEOUT:
                    logout(request, 'login.html')
            request.session['last_active_time'] = current_datetime
        response = self.get_response(request)
        return response
