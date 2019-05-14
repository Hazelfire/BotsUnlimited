"""
File: client.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: defines a generic client entry
"""

from botsunlimited.util import wrap_bot
from . import routes as bot_routes


async def run_routes(routes, message):
    """Runs the routes on a given message

    :routes: defined routes to controllers
    :message: discord message object

    """
    for route in routes:
        await route.run(message)


async def on_message(message):
    """callback for discord.py"""
    run_routes(bot_routes, message)


def get_client():
    """Returns a client for sarah"""
    return wrap_bot(on_message)
