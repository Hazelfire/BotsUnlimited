from .reqs import has_words, always, mentioned
from . import views


def route(req, view):
    """ Defines a route to a controller """

    async def run(client, message):
        if req(message, client):
            return await view(client, message)

    return run


def group(req, routes):
    async def run(client, message):
        if req(message, client):
            for route in routes:
                await route(client, message)

    return run


routes = [group(mentioned(), [route(always(), views.introduce_myself)])]
