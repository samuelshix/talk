import os

import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from landing import consumers
import landing.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialnetwork.settings')
django.setup()

application = ProtocolTypeRouter({
  # "http": AsgiHandler(),
  "websocket": AuthMiddlewareStack(
      URLRouter(
          landing.routing.websocket_urlpatterns
      )
  )
  # Just HTTP for now. (We can add other protocols later.)
})