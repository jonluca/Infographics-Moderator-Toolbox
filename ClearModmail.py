from threading import Thread
import time
from CommonUtils import get_reddit_instance

reddit = get_reddit_instance("/r/dankmemes ModmailClearer v1.0 by /u/larperdoodle")
subreddit = reddit.subreddit('/r/dankmemes')
while True:
	for conversation in subreddit.conversations(state='new'):
		if len(conversation.messages) == 1:
			for message in conversation.messages:
				if message.startswith("Thank you for submitting to"):
							Thread(target=conversation.archive).start()

	time.sleep(3)
