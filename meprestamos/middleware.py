from django.conf import settings
from django.http import HttpResponsePermanentRedirect

class RedirectToCustomDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host == 'mar-eriprestamos-cold-cherry-2402.fly.dev':
            return HttpResponsePermanentRedirect(f"https://mar-eriprestamos.com{request.path}")
        return self.get_response(request)