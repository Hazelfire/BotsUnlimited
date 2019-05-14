import discord


def wrap_bot(on_message):
    client = discord.Client()
    client.event(on_message)
    return client
