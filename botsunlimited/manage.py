import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DMVC_SETTINGS_MODULE", "botsunlimited.settings")
    from discordmvc import run

    run()
