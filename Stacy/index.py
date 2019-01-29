import discord
import os
import asyncio
from dateutil.parser import parse
from googlecalendar import get_upcoming, patch_event
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

def event_to_string(event):
    time = ""
    if 'dateTime' in event['start']:
        time =  parse(event["start"]["dateTime"]).strftime("%A, %d of %B at %I:%M%p")
    else:
        time =  parse(event["start"]["date"]).strftime("%A, %d of %B")
    return event["summary"] + ", " + time

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

plan_calendar = 'rmit.edu.au_ct5j003ncdbmu1o2ga2gasu86k@group.calendar.google.com'

def parse_datetime(date):
    return parse(date).strftime("%A, %d of %B at %I:%M%p")

def parse_time(date):
    return parse(date).strftime("%I:%M%p")

def parse_date(date):
    return parse(date).strftime("%A, %d of %B")



def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html.replace("<br>", "\n"))
    return cleantext

def event_time_to_string(start, end):
    if start["dateTime"]:
        return 'from {} to {}'.format(parse_datetime(start["dateTime"]), parse_time(end["dateTime"]))
    else:
        return 'on {}'.format(parse_date(start["date"]))

async def describe_event(channel, event):
    await client.send_message(channel,
            content='Certainly, the {} will be run {} \n Location: {}\n{}'.format(
                event["summary"],
                event_time_to_string(event["start"], event["end"]),
                event['location'] if 'location' in event else 'Undecided',
                cleanhtml(event["description"]) if 'description' in event else 'Description Needed'
            ))

async def on_event_match(message, event):
    location_set = re.search('(?:at|in) (\d\d\.\d\d\.\d\d\d)', message.content)
    if location_set:
        room_no = location_set.group(1)
        patch_event(plan_calendar, event["id"], {"location": room_no})
        await client.send_message(message.channel, "Ok, set {} to location {}".format(event["summary"], room_no))
    else:
        await describe_event(message.channel, event)


@client.event
async def on_message(message):
    name = message.author.nick if hasattr(message.author, 'nick') and message.author.nick is not None else message.author.name
    if client.user.mentioned_in(message):
        if not message.channel.is_private and message.author.server_permissions.administrator:
            await client.send_typing(message.channel)
            events = get_upcoming(plan_calendar);
            event = match_event(message.content, events)

            if event: 
                await on_event_match(message, event)                
            else:
                if words_in(['plan', 'event', 'run', 'schedule'], message.content):
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
