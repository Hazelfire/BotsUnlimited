from .models import Event
from fuzzywuzzy import fuzz


def mentioned():
    def req(message, client):
        return client.user.mentioned_in(message)

    return req


def always():
    def req(message, client):
        return True

    return req


def has_words(*words):
    def req(message, client):
        for word in words:
            if word in message.content:
                return True
        return False

    return req


def has_event():
    def req(message):
        events = Event
        query = message.content
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

    return req
