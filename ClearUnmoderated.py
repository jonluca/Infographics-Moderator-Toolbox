import time
from CommonUtils import get_reddit_instance, hours_since

reddit = get_reddit_instance("/r/dankmemes UnmoderatedClearer v3.0 by /u/AdamZF")
sub = reddit.subreddit('dankmemes')
numApproved = 0

while True:
	for submission in sub.mod.unmoderated(limit=None):
		hours = hours_since(submission.created_utc)
		if submission.score < 10:
			if hours > 1:
				Thread(target=submission.mod.remove).start()
		else:
			if hours > 23:
				Thread(target=submission.mod.approve).start()
	time.sleep(30)