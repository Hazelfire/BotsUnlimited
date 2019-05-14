from discordmvc.reqs import always, mentioned, has_words
from discordmvc.routes import route, group
from . import views


routes = [
    group(
        mentioned(),
        [
            route(has_words("events"), views.list_events),
            route(always(), views.introduce_myself),
        ],
    )
]
