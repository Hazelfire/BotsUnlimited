import discord
import os
import asyncio
from dateutil.parser import parse
from .googlecalendar import get_upcoming
from fuzzywuzzy import fuzz
import re
import json
from unione import get_member_count

client = discord.Client()
db_file = os.path.expanduser("~/.config/bots/db.json")

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

def is_yes(text):
    return 'yes' in text.lower() or 'sure' in text.lower() or 'yeah' in text.lower()

async def get_rating(minn, maxn, author):
    while True:
        reply = await client.wait_for_message(author=author)
        if reply.content.isdigit():
            rating = int(reply.content)
            if rating >= minn:
                if rating <= maxn:
                    return rating
                else:
                    await client.send_message(author, "Wow a {}, I'm completely flattered! However even if you are that impressed a {} would be enough for us. Mind if you could give your rating again?".format(rating, maxn))
            else:
                await client.send_message(author, "Damn, sorry to hear that. Sadly my analytics software I'm using only has a minimum entry of {}.  Mind if you could give your rating again?".format(minn, rating))
        else:
            await client.send_message(author, "Sorry, but I'm looking for a whole number between {} and {}".format(minn, maxn))



async def get_feedback(author, event):
    name = author.nick if hasattr(author, 'nick') and author.nick is not None else author.name
    
    await client.send_message(author, "Hey {}, I noticed that you attended the {}. Can I ask you some questions about how it went so that we can get better?".format(name, event))
    reply = await client.wait_for_message(author=author)
    if is_yes(reply.content):
        feedback = {}
        await client.send_message(author, "Thank you so much! First question (got four in total), from 1 to 5, did you enjoy it? Would you come to a similar event in the future?")
        feedback["rating"] = await get_rating(1, 5, author)

        await client.send_message(author, "Second question (classic, brace yourself), from 1 to 5, would you recommend the event to a friend?")
        feedback["recommend"] = await get_rating(1, 5, author)

        await client.send_message(author, "Third question (2 more to go), what did you like about this event?")
        reply = await client.wait_for_message(author=author)
        feedback["positive"] = reply.content

        await client.send_message(author, "Last question (and my personal favourite), what can we do to improve?")
        reply = await client.wait_for_message(author=author)
        feedback["improve"] = reply.content

        await client.send_message(author, "Thank you SO MUCH. You have no idea what this feedback means to us. Have a wonderful day")

        return feedback
    else:
        await client.send_message(author, "That's totally ok. Have a nice day")



@client.event
async def on_message(message):
    name = message.author.nick if hasattr(message.author, 'nick') and message.author.nick is not None else message.author.name
    if client.user.mentioned_in(message):
        with open(db_file, "r+") as f:
            users = json.load(f)
            if message.author.id in users:
                if words_in(["test"],  message.content):
                    await client.send_message(message.channel, "Sure! I'll just test out the feeback giving process with you")
                    await get_feedback(message.author, "Test event")
                elif words_in(["many","count"], message.content):
                    await client.send_message(message.channel, "I'll quickly check, give me a second")
                    await client.send_typing(message.channel)
                    count = await get_member_count()
                    await client.send_message(message.channel, "We currently have {} members!".format(count))
                else:
                    await client.send_message(message.channel, content="Hey {}, I'm Maggie, Senior director for Program Management. I take feedback on events as well as give data".format(name))
            else:
                await client.send_message(message.channel, "Hey {}! I don't think I've met you before. I'm Maggie. Would you like to join the analytics program?\nI don't do much, I just gather feedback from you after events. This feedback is entirely anonymous".format(name))
                reply = await client.wait_for_message(author=message.author, channel=message.channel)
                if is_yes(reply.content):
                    await client.send_message(message.author, "So that I can know who you are when you register on eventbrite, can you tell me your student number (with the s?)".format(name))
                    response = await client.wait_for_message(author=message.author)
                    users[response.author.id] = response.content
                    f.seek(0)
                    json.dump(users, f)
                    await client.send_message(message.author, "Thank you! I've got you in the system now")
