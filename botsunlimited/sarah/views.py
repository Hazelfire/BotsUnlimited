from .models import Event


async def list_events(client, message, context):
    events = list(context.db.query(Event).all())
    await message.channel.send(
        context.templates.get_template("events.jinj").render({"events": events})
    )
