"""
File: __init__.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Entry point for discordmvc module
"""
from .util import create_client
from .cli import cli
from importlib import import_module
import os
import asyncio


async def arun(bots):
    await asyncio.gather(*[create_client(bot).start(token) for bot, token in bots])


def run(arguments):
    settings = import_module(os.environ["DMVC_SETTINGS_MODULE"])
    applications = settings.APPLICATIONS
    print("Running bots")
    asyncio.get_event_loop().run_until_complete(arun(applications))
