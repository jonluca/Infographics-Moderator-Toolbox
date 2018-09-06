import time
from CommonUtils import hours_since
from CommonUtils import get_reddit_instance
from threading import Thread

reddit = get_reddit_instance("/r/dankmemes ClearControversial v3.0 by /u/AdamZF")

sub = reddit.subreddit('dankmemes')

while True:
	for submission in sub.controversial('day', limit=None):
		if submission.score < 10:
			hours = hours_since(submission.created_utc)
			if hours > 1:
				submission.mod.remove()
				Thread(target=submission.mod.remove).start()
	time.sleep(30)

