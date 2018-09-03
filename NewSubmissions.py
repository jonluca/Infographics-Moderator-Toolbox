import sqlite3
import time

from CommonUtils import get_reddit_instance


def process_submission(submission):
    checked = check_db(submission)
    if not checked:
        comment = submission.reply(
            "#Upvote this comment if this is an **infographic**. Downvote this comment if this is a spam, or an *image with text*. Note that if the entire submissions could instead be a text post (the visuals don't matter), this is **not** an infographic!.")
        comment.mod.distinguish(how='yes', sticky=True)
        comment.mod.approve()
        add_comment_db(comment, submission)


def add_comment_db(comment, submission):
    conn = sqlite3.connect('infographics.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comments(comment_id, parent_post, reported)''')
    comment_id = comment.id
    post_id = submission.id
    c.execute('''INSERT INTO comments(comment_id, parent_post) VALUES(?,?)''', (comment_id, post_id))
    conn.commit()
    conn.close()


def check_db(submission):
    conn = sqlite3.connect('infographics.db')
    c = conn.cursor()
    post_id = submission.id
    posts_db = c.execute('''SELECT * FROM comments WHERE parent_post=? LIMIT 1''', [post_id])
    conn.commit()
    if posts_db.fetchone():
        conn.close()
        return "found"
    else:
        conn.close()
        return


conn = sqlite3.connect('infographics.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS comments (comment_id, parent_post, reported)''')
conn.commit()
conn.close()

reddit = get_reddit_instance("/r/infographics SubmissionChecker by /u/JonLuca")

sub = reddit.subreddit('infographics')
print("Starting Script")
while True:
    for submission in sub.new(limit=100):
        process_submission(submission)
        time.sleep(30)
