"""
File: util.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Util file for constructing discord.py clients from projects
"""

import os
import discord


async def run_routes(routes, message, client):
    """Runs the given routes with the message
    :routes: an array of route objects
    :message: Discord.py message

    """
    for route in routes:
        await route(client, message)


def wrap_bot(on_message):
    """Creates a bot from an async on_message function

    :on_message: async discord.py on_message function
    :returns: Discord.py Client

    """
    client = discord.Client()
    client.event(on_message(client))
    return client


def create_client(module):
    """Creates a discord client based off project settings
    :returns: Discord.py client

    """
    routes = __import__(module + ".routes").routes.routes

    def wrapper(client):
        async def on_message(message):
            """Discord.py on_message function

            :message: Discord.py message

            """
            await run_routes(routes, message, client)

        return on_message

    return wrap_bot(wrapper)
