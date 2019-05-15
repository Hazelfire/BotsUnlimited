from .models import Event
from discordmvc.actions import reply


async def list_events(client, message, context):
    events = list(context.db.query(Event).all())
    yield reply(events=events)
