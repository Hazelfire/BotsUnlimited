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
