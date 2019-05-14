def route(req, view):
    """ Defines a route to a controller """

    async def run(client, message, context):
        if req(message, client):
            return await view(client, message, context)

    return run


def group(req, routes):
    async def run(client, message, context):
        if req(message, client):
            for route in routes:
                result = await route(client, message, context)
                if result:
                    return result

    return run
