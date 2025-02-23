"""
ASGI config for zodiac project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
"""
import os
from django.core.asgi import get_asgi_application
from whitenoise import WhiteNoise


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zodiac.settings')

application = get_asgi_application()

application = WhiteNoise(application, root='/path/to/static/files', prefix='static/')
"""
import os
from django.core.asgi import get_asgi_application
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zodiac.settings')

wsgi_app = get_wsgi_application()
wsgi_app = WhiteNoise(wsgi_app, root='', prefix='static/')

asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'http': asgi_app
})
