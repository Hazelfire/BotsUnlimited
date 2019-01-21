import discord
import os
import asyncio
from dateutil.parser import parse
from googlecalendar import get_upcoming
from fuzzywuzzy import fuzz
import re

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def words_in(words, message):
    for word in words:
        if word in message:
            return True
    return False

def match_event(query, events):
    fuzzy_threshold_ratio = 90
    
    max_event = None
    max_ratio = 0
    for event in events:
        ratio = fuzz.partial_ratio(event["summary"].lower(), query.lower()) 
        if ratio > max_ratio:
            max_ratio = ratio
            max_event = event

    if max_ratio > fuzzy_threshold_ratio:
        return max_event
    return None

def parse_datetime(date):
    return parse(date).strftime("%A, %d of %B at %I:%M%p")

def parse_time(date):
    return parse(date).strftime("%I:%M%p")


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html.replace("<br>", "\n"))
    return cleantext


@client.event
async def on_message(message):
    name = message.author.nick if hasattr(message.author, 'nick') and message.author.nick is not None else message.author.name
    if client.user.mentioned_in(message):
        await client.send_typing(message.channel)
        events = get_upcoming();
        event = match_event(message.content, events)
        if event:
            await client.send_message(message.channel,
                    content='Certainly, the {} will be run from {} to {} \n Location: {}\n{}'.format(
                        event["summary"],
                        parse_datetime(event["start"]["dateTime"]),
                        parse_time(event["end"]["dateTime"]),
                        event["location"],
                        cleanhtml(event["description"])
                    ))
        elif words_in(['event', 'run', 'schedule'], message.content):
            upcoming = "\n".join([event["summary"] + ", " + parse_datetime(event["start"]["dateTime"]) for event in events])
            await client.send_message(message.channel, content='Certainly {}, Our Upcoming events are \n {}'.format(name, upcoming))
        else:
            await client.send_message(message.channel, content="Hey {}, I'm Sarah, VP of marketing operations here at Bots Unlimited. I don't check Discord often, so if you want to talk to me, please mention me. You can ask me about what events are coming up".format(name))

client.run(os.environ["SARAH_TOKEN"])
