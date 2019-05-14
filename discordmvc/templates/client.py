"""
File: client.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Exposes a client for use in other projects
"""
import os
from discordmvc import create_client

os.environ.setdefault("DISCORDMVC_SETTINGS", "botsunlimited.settings")

client = create_client()
