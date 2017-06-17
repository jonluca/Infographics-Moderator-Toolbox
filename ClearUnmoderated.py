import time

from CommonUtils import get_reddit_instance, hours_since

reddit = get_reddit_instance()
sub = reddit.subreddit('dankmemes')

while True:
    # Remove any post with less than 10 upvotes in the first hour
    # Approve any post that is more than 24 hours old
    for submission in sub.mod.unmoderated(limit=None):
        hours = hours_since(submission.created_utc)
        if submission.score < 10:
            if hours > 1:
                submission.mod.remove()
        else:
            if hours > 23:
                submission.mod.approve()
        time.sleep(3)
