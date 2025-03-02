from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not request.session.get('last_activity'):
            request.session['last_activity'] = request.session.get('_session_expiry')

        if request.user.is_authenticated and request.session.get('last_activity'):
            last_activity = request.session['last_activity']
            from datetime import datetime
            now = datetime.now()
            if (now - last_activity).seconds > 300:  # 5 minutos
                del request.session['last_activity']
                return redirect(reverse('login'))  # Redireciona para a página de login

        return None