from eventbrite import Eventbrite
from dateutil.parser import parse
import os

eventbrite = Eventbrite(os.environ["EVENTBRITE_TOKEN"])


def format_time(original):
    return parse(original).strftime("%Y-%m-%dT%H:%M:%SZ")


def list_events():
    organisation = "18168938480"
    return eventbrite.get(
        "/organisations/{}/events/".format(organisation), {"time-filter": "past"}
    )
