"""
File: util.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Util file for constructing discord.py clients from projects
"""

import os
import discord
from jinja2 import Environment, PackageLoader, select_autoescape


async def run_routes(routes, message, client, context):
    """Runs the given routes with the message
    :routes: an array of route objects
    :message: Discord.py message

    """
    for route in routes:
        await route(client, message, context)


def wrap_bot(on_message):
    """Creates a bot from an async on_message function

    :on_message: async discord.py on_message function
    :returns: Discord.py Client

    """
    client = discord.Client()
    client.event(on_message(client))
    return client


class Context:
    def __init__(self, templates):
        self.templates = templates


def create_client(module):
    """Creates a discord client based off project settings
    :returns: Discord.py client

    """
    routes = __import__(module + ".routes").routes.routes
    templates = Environment(
        loader=PackageLoader(module, "templates"), autoescape=select_autoescape([])
    )

    def wrapper(client):
        async def on_message(message):
            """Discord.py on_message function

            :message: Discord.py message

            """
            await run_routes(routes, message, client, Context(templates))

        return on_message

    return wrap_bot(wrapper)
