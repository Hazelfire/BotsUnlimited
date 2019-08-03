from discordmvc.reqs import always, mentioned, has_words
from discordmvc.routes import route, group
from . import views
from botsunlimited.views import introduce


def routes(client, message, context):
    if client.user.mentioned_in(message):
        if "events" in message.content:
            return views.list_events
        return introduce
