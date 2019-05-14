def route(req, view):
    """ Defines a route to a controller """

    def run(client, message):
        if req(message, client):
            return view

    return run


def group(req, routes):
    def run(client, message):
        if req(message, client):
            for route in routes:
                result = route(client, message)
                if result:
                    return result

    return run
