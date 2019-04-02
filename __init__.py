from .brent import client as brent_client
from .sarah import client as sarah_client
from .stacy import client as stacy_client
from .maggie import client as maggie_client
import os
import asyncio

async def run_bots():
    await asyncio.gather(
        brent_client.start(os.environ["BRENT_TOKEN"]),
        sarah_client.start(os.environ["SARAH_TOKEN"]),
        maggie_client.start(os.environ["MAGGIE_TOKEN"]),
        stacy_client.start(os.environ["STACY_TOKEN"]),
    )
async def get_bots():
    await brent_client.login(os.environ["BRENT_TOKEN"])
    await sarah_client.login(os.environ["SARAH_TOKEN"])
    await stacy_client.login(os.environ["STACY_TOKEN"])
    await maggie_client.login(os.environ["MAGGIE_TOKEN"])
    return [
        brent_client,
        sarah_client,
        stacy_client,
        maggie_client
    ]
