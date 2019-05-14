from jinja2 import Environment, PackageLoader, select_autoescape


async def introduce_myself(client, message):
    env = Environment(loader=PackageLoader("sarah", "templates"))
    await message.channel.send(env.get_template("intro.jinj").render(message=message))
