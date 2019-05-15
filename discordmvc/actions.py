def reply(**kwargs):
    async def wraps(client, message, context, view):
        await message.channel.send(
            context.templates.get_template(view + ".jinj").render(
                message=message, **kwargs
            )
        )

    return wraps


def reply_to(message):
    def check(m):
        return message.author == m.author and message.channel == m.channel

    return check


def listen():
    async def wraps(client, message, context, view):
        return await client.wait_for("message", check=reply_to(message))

    return wraps


def query(**kwargs):
    async def wraps(client, message, context, view):
        await reply(**kwargs)(client, message, context, view)
        return await listen()(client, message, context, view)

    return wraps
