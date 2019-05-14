from jinja2 import Environment, PackageLoader, select_autoescape


async def introduce_myself(client, message, context):
    await message.channel.send(
        context.templates.get_template("intro.jinj").render(message=message)
    )
