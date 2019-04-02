import discord
import asyncio
from dateutil.parser import parse
from .googlecalendar import get_upcoming
from fuzzywuzzy import fuzz
import os

client = discord.Client()

def words_in(words, message):
    for word in words:
        if word in message.lower():
            return True
    return False

def event_to_string(event):
    time = ""
    if 'dateTime' in event['start']:
        time =  parse(event["start"]["dateTime"]).strftime("%A, %d of %B at %I:%M%p")
    else:
        time =  parse(event["start"]["date"]).strftime("%A, %d of %B")
    return event["summary"] + ", " + time

async def print_calendar(events, event_type, channel):
    if len(events) > 0:
        upcoming = "\n".join([event_to_string(event) for event in events])
        counter = 0
        await client.send_message(channel, content='Here are the {} we have planned: \n {}'.format(event_type, upcoming))
    else:
        await client.send_message(channel, "No {} planned".format(event_type))

def match_event(query, events):
    fuzzy_threshold_ratio = 90
    
    max_ratio = 0
    max_event = None
    for event in events:
        ratio = fuzz.partial_ratio(event["summary"].lower(), query.lower()) 
        if ratio > max_ratio:
            max_ratio = ratio
            max_event = event

    if max_ratio > fuzzy_threshold_ratio:
        return max_event
    return None

plan_calendar = 'rmit.edu.au_ct5j003ncdbmu1o2ga2gasu86k@group.calendar.google.com'

@client.event
async def on_message(message):
    name = message.author.nick if hasattr(message.author, 'nick') and message.author.nick is not None else message.author.name
    if client.user.mentioned_in(message):
        if not message.channel.is_private and message.author.server_permissions.administrator:
            await client.send_message(message.channel, "Hi {}, I'm Brent, Operations Officer here at Bots Unlimited. I can publish Eventbrite events".format(name))
        else:
            await client.send_message(message.channel, "Hi {}, I'm Brent, Operations Officer here at Bots Unlimited. I do operations work for executive".format(name))

