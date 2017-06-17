import datetime
import os

import praw
from datetime import timedelta


def hours_since(timestamp):
    current_time = datetime.datetime.utcnow() - timedelta(hours=5)
    sub_time = datetime.datetime.fromtimestamp(timestamp)
    diff = current_time - sub_time
    return round(diff.total_seconds() / 3600)


def get_settings(filename):
    settings = []
    try:
        if not os.path.exists(filename):
            raise IOError
        with open(filename) as file:
            for line in file:
                line = str(line.strip())
                settings.append(line)
        try:
            file.close()
        except:
            pass
    except IOError:
        pass
    except:
        pass
    return settings


def get_reddit_instance():
    settings = get_settings("settings.txt")
    return praw.Reddit(client_id=settings[0],
                       client_secret=settings[1],
                       username=settings[2],
                       user_agent=settings[3],
                       password=settings[4])
