from eventbrite import Eventbrite
from dateutil.parser import parse
eventbrite = Eventbrite('BJIR7LYMPTMJPYVEAT2R')

def format_time(original):
    return parse(original).strftime("%Y-%m-%dT%H:%M:%SZ")

def list_events():
    return eventbrite.post_event({
        "event": {
            "name": {
                "html": event["summary"]
            },
            "description": {
                "html": event["description"]
            },
            "start": {
                "timezone": "Australia/Melbourne",
                "utc": format_time(event["start"]["dateTime"])
            },
            "end": {
                "timezone": "Australia/Melbourne",
                "utc": format_time(event["end"]["dateTime"])
            },
            "currency": "AUD",
            "capacity": 100,
        }
    })
