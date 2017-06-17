import datetime
import praw
from datetime import timedelta


def hours_since(timestamp):
    current_time = datetime.datetime.utcnow() - timedelta(hours=5)
    sub_time = datetime.datetime.fromtimestamp(timestamp)
    diff = current_time - sub_time
    return round(diff.total_seconds() / 3600)


def get_reddit_instance():
    return praw.Reddit(client_id='',
                       client_secret='',
                       username='',
                       user_agent='',
                       password='')
