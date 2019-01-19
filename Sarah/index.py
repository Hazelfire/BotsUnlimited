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

@client.event
async def on_message(message):
    name = message.author.nick if hasattr(message.author, 'nick') else message.author.name
    if client.user.mentioned_in(message):
        if words_in(['event', 'run', 'schedule'], message.content):
            await client.send_typing(message.channel)
            events = get_upcoming();
            upcoming = "\n".join([event["summary"] + ", " + parse(event["start"]["dateTime"]).strftime("%A, %d of %B at %I:%M%p") for event in events])
            counter = 0
            await client.send_message(message.channel, content='Certainly {}, Our Upcoming events are \n {}'.format(name, upcoming))
        else:
            await client.send_message(message.channel, content="Hey {}, I'm Sarah, VP of marketing operations here at Bots Unlimited. I don't check Discord often, so if you want to talk to me, please mention me. You can ask me about what events are coming up".format(name))

client.run(os.environ["SARAH_TOKEN"])
