from sarah.models import Event


async def list_plan(client, message, context):
    events = list(context.db.query(Event).all())
    await message.channel.send(
        context.templates.get_template("events.jinj").render({"events": events})
    )


def reply_to(message):
    def check(m):
        return message.author == m.author and message.channel == m.channel

    return check


async def create_event(client, message, context):
    await message.channel.send(
        context.templates.get_template("create_event.jinj").render({"stage": "name"})
    )

    name_response = await client.wait_for("message", check=reply_to(message))
    name = name_response.content
    await message.channel.send(
        context.templates.get_template("create_event.jinj").render(
            {"name": name, "stage": "description"}
        )
    )

    description_response = await client.wait_for("message", check=reply_to(message))
    description = description_response.content

    context.db.add(Event(name=name, description=description))
    await message.channel.send(
        context.templates.get_template("create_event.jinj").render(
            {"name": name, "stage": "end"}
        )
    )


async def delete_event(client, message, context):
    events = list(context.db.query(Event).all())
    await message.channel.send(
        context.templates.get_template("delete_event.jinj").render(
            {"stage": "list-events", "events": events}
        )
    )

    name_response = await client.wait_for("message", check=reply_to(message))
    name = name_response.content

    event = context.db.query(Event).filter(Event.name == name).first()
    if event:
        await message.channel.send(
            context.templates.get_template("delete_event.jinj").render(
                {"stage": "confirm", "event": event}
            )
        )

        confirm_response = await client.wait_for("message", check=reply_to(message))
        confirm = confirm_response.content
        if confirm.upper() == "YES":
            context.db.query(Event).filter(Event.name == name).delete()

            await message.channel.send(
                context.templates.get_template("delete_event.jinj").render(
                    {"stage": "done"}
                )
            )
        else:
            await message.channel.send(
                context.templates.get_template("delete_event.jinj").render(
                    {"stage": "cancel"}
                )
            )

    else:
        await message.channel.send(
            context.templates.get_template("delete_event.jinj").render(
                {"stage": "missing"}
            )
        )
