#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __main__.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Runs the client
"""
import os
from .client import client

settings = __import__(os.environ["DISCORDMVC_SETTINGS"])
client.run(settings.token)
