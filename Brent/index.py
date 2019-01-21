import discord
import asyncio
from dateutil.parser import parse
from googlecalendar import get_upcoming
from fuzzywuzzy import fuzz
import os
from pusheventbrite import create_event

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

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
    name = message.author.nick if message.author.nick is not None else message.author.name
    if client.user.mentioned_in(message):
        if message.author.server_permissions.administrator:
            if words_in(['eventbrite'], message.content):
                max_ratio = 0
                request = message.content
                events = [event for event in get_upcoming(plan_calendar) if 'dateTime' in event["start"] and 'description' in event]
                while max_ratio <= 90:
                    await client.send_typing(message.channel)
                    fuzzy_threshold_ratio = 90
                    
                    event = match_event(request, events)

                    if event:
                        await client.send_message(message.channel, "So you want to publish {} to Eventbrite?".format(event['summary']))
                        reply = await client.wait_for_message(channel=message.channel, author = message.author)
                        if reply.content.lower() == "yes":
                            await client.send_message(message.channel, "Alrighty, I'll get on to it")
                            await client.send_typing(message.channel)
                            print(create_event(event))
                            await client.send_message(message.channel, "All done with creating an event for {}. Let me know if you need anything more".format(event["summary"]))
                        else:
                            await client.send_message(message.channel, "Ok, I'll hold it off")
                        break

                    else: 
                        await client.send_message(message.channel, "What event do you want to publish?")
                        await print_calendar(events, "events", message.channel)
                        reply = await client.wait_for_message(channel=message.channel, author=message.author)
                        request = reply.content
            else:
                await client.send_message(message.channel, "Hi {}, I'm Brent, Operations Officer here at Bots Unlimited. I can publish Eventbrite events".format(name))
        else:
            await client.send_message(message.channel, "Hi {}, I'm Brent, Operations Officer here at Bots Unlimited. I do operations work for executive".format(name))



client.run(os.environ["BRENT_TOKEN"])
