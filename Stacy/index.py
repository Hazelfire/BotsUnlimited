import discord
import os
import asyncio
from dateutil.parser import parse
from googlecalendar import get_upcoming

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

def event_to_string(event):
    time = ""
    if 'dateTime' in event['start']:
        time =  parse(event["start"]["dateTime"]).strftime("%A, %d of %B at %I:%M%p")
    else:
        time =  parse(event["start"]["date"]).strftime("%A, %d of %B")
    return event["summary"] + ", " + time

@client.event
async def on_message(message):
    name = message.author.nick if hasattr(message.author, 'nick') and message.author.nick is not None else message.author.name
    if client.user.mentioned_in(message):
        if message.author.server_permissions.administrator:
            if words_in(['plan', 'event', 'run', 'schedule'], message.content):
                await client.send_typing(message.channel)
                events = get_upcoming('rmit.edu.au_ct5j003ncdbmu1o2ga2gasu86k@group.calendar.google.com');
                if len(events) > 0:
                    upcoming = "\n".join([event_to_string(event) for event in events if 'dateTime' in event['start'] and 'description' in event and 'location' in event])
                    messages = []
                    counter = 0
                    if len(upcoming) > 0:
                        messages.append('Here are the events we have planned: \n {}'.format(upcoming))
                    else: 
                        messages.append('We don\'t actually have any events completely ready to publish yet')

                    no_time = "\n".join([event_to_string(event) for event in events if 'dateTime' not in event['start']])
                    
                    if len(no_time) > 0:
                        messages.append('These ones we haven\'t got a specific time for: \n {}'.format(no_time))

                    no_description = "\n".join([event_to_string(event) for event in events if 'description' not in event])
                    if len(no_description) > 0:
                        messages.append('These ones don\'t have a description: \n {}'.format(no_description))

                    no_location = "\n".join([event_to_string(event) for event in events if 'location' not in event])
                    if len(no_description) > 0:
                        messages.append('These ones don\'t have a location: \n {}'.format(no_location))
                    await client.send_message(message.channel, content="\n\n".join(messages))
                else:
                    await client.send_message(message.channel, "No events planned")
            elif words_in(['meeting'], message.content):
                await client.send_typing(message.channel)
                events = get_upcoming('rmit.edu.au_cqqvahbep63tttoc551ug04q88@group.calendar.google.com');
                if len(events) > 0:
                    upcoming = "\n".join([event_to_string(event) for event in events])
                    counter = 0
                    await client.send_message(message.channel, content='Here are the meetings we have planned: \n {}'.format(upcoming))
                else:
                    await client.send_message(message.channel, "No meetings coming up")
            else:
                await client.send_message(message.channel, content="Hey {}, I'm Stacy, Assistant here at Bots Unlimited. I can tell you about meetings and events that are planned but not published".format(name))
        else:
            await client.send_message(message.channel, content="Hey {}, I'm Stacy, Assistant here at Bots Unlimited. I'm only available to executive".format(name))

client.run(os.environ["STACY_TOKEN"])
