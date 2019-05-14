from discordmvc.reqs import always, mentioned
from discordmvc.routes import route, group
from . import views


routes = [group(mentioned(), [route(always(), views.introduce_myself)])]
