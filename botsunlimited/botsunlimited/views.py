async def introduce(client, message, context):
    await message.channel.send(context.templates.get_template("intro.jinj").render())
