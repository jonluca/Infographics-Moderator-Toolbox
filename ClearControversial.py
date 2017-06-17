import time
from CommonUtils import hours_since
from CommonUtils import get_reddit_instance

reddit = get_reddit_instance()

sub = reddit.subreddit('dankmemes')

while True:
    for submission in sub.controversial('day', limit=None):
        if submission.score < 10:
            hours = hours_since(submission.created_utc)
            if hours > 1:
                submission.mod.remove()
                time.sleep(3)
    time.sleep(3)
