from CommonUtils import get_reddit_instance

reddit = get_reddit_instance("/r/infographis UnmoderatedClearer v3.0 by /u/JonLuca")
sub = reddit.subreddit('infographics')
numApproved = 0
for submission in sub.mod.unmoderated(limit=None):
    submission.mod.approve()
    numApproved += 1
    print("Approved " + str(numApproved))
