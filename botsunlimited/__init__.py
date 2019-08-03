""" Bots unlimited module """
from discordmvc import get_bots

def bots():
    """ Returns all the bots in this application """
    return get_bots("botsunlimited.settings")
