from jinja2 import Environment, PackageLoader, select_autoescape
from .models import Event


async def introduce_myself(client, message, context):
    await message.channel.send(
        context.templates.get_template("intro.jinj").render(message=message)
    )


async def list_events(client, message, context):
    events = list(context.db.query(Event).all())
    if len(events) == 0:
        await message.channel.send("No events have been registered")
    else:
        await message.channel.send("\n".join([event.name for event in events]))
