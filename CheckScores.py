import sqlite3
import time

from CommonUtils import get_reddit_instance


def remove_post(comment, reddit):
    conn = sqlite3.connect('infographics.db')
    c = conn.cursor()
    comment_id = comment.id
    posts_db = c.execute('''SELECT * FROM comments WHERE comment_id=?''', [comment_id]).fetchone()
    current = posts_db[1]
    post = reddit.submission(current)
    post.mod.remove()
    c.execute('''UPDATE comments SET reported="yes" WHERE comment_id =?''', [comment_id])
    conn.commit()
    conn.close()


def report_post(comment, reddit):
    conn = sqlite3.connect('infographics.db')
    c = conn.cursor()
    comment_id = comment.id
    posts_db = c.execute('''SELECT * FROM comments WHERE comment_id=?''', [comment_id]).fetchone()
    current = posts_db[1]
    post = reddit.submission(current)
    # msg_sub = reddit.subreddit('infographics')
    # post_link = post.shortlink
    # message_send = 'Mods, Please check this post, it reached the downvote threshold.  [Link](%s)' % post_link
    # msg_sub.message('Check Post', message_send)
    post.report("Not an infographic.")
    c.execute('''UPDATE comments SET reported="yes" WHERE comment_id =?''', [comment_id])
    conn.commit()
    conn.close()


time.sleep(1)
conn = sqlite3.connect('infographics.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS comments (comment_id, parent_post, reported)''')
conn.commit()
conn.close()

reddit = get_reddit_instance("/r/infographics CheckCommentScores by /u/JonLuca")

user = reddit.redditor('Infographics_Mod')
print("Starting check score script")
while True:
    for comment in user.comments.new(limit=400):
        comment_id = comment.id
        conn = sqlite3.connect('infographics.db')
        c = conn.cursor()
        posts_db = c.execute('''SELECT * FROM comments WHERE comment_id=?''', [comment_id]).fetchone()
        if posts_db:
            removed = posts_db[2]
            if removed == "yes":
                conn.close()
                continue
            else:
                conn.close()
                if comment.score < -6:
                    report_post(comment, reddit)
                elif comment.score < -20:
                    remove_post(comment, reddit)
        time.sleep(30)
