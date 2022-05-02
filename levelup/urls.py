from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user
from rest_framework import routers
from levelupapi.views import GameTypeView, EventView, GameView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'events', EventView, 'event')
router.register(r'games', GameView, 'game')
# trailing_slash=False tells the router to accept "/gametypes" instead of"/gametypes/
# the next line is what sets up the /gametypes resource. The first parameter, r'gametypes, is setting
# up the url. The second "GameTypeView" is telling the server which view to use when it sees that url.
# The 3rd, 'gametype', is called the base name. You'll only see the base name if you get an error.


urlpatterns = [
# Requests to http://localhost:8000/register will be routed to the register_user function
# Requests to http://localhost:8000/login will be routed to the login_user function
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

