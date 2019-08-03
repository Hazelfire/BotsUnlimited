from discordmvc.reqs import always, mentioned, has_words
from discordmvc.routes import route, group
from . import views
from botsunlimited.views import introduce


def routes(client, message, context):
    if client.user.mentioned_in(message):
        if "plan" in message.content:
            return views.list_plan
        elif "create" in message.content:
            return views.create_event
        elif "delete" in message.content:
            return views.delete_event
        return introduce
