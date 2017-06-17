import praw
import re
import sqlite3
import time
import threading
from threading import Thread
import datetime
from datetime import timedelta


def new_submissions():
    conn = sqlite3.connect('dankmemes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comments (comment_id, parent_post, reported)''')
    conn.commit()
    conn.close()


    reddit = praw.Reddit(client_id = '',
                        client_secret = '',
                        username = '',
                        user_agent = '',
                        password = '')

    sub = reddit.subreddit('dankmemes')

    for submission in sub.new(limit=100):
        process_submission(submission)
        time.sleep(2)

def add_comment_db(comment, submission):
    conn = sqlite3.connect('dankmemes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comments(comment_id, parent_post, reported)''')
    comment_id = comment.id
    post_id = submission.id
    c.execute('''INSERT INTO comments(comment_id, parent_post) VALUES(?,?)''', (comment_id, post_id))
    conn.commit()
    conn.close()

def check_db(submission):
    conn = sqlite3.connect('dankmemes.db')
    c = conn.cursor()
    post_id = submission.id
    posts_db = c.execute('''SELECT * FROM comments WHERE parent_post=? LIMIT 1''',[post_id])
    conn.commit()
    if posts_db.fetchone():
        conn.close()
        return "found"
    else:
        conn.close()
        return

def process_submission(submission):
    check = check_db(submission)
    if(check):
        pass
    else:
        comment = submission.reply("#Upvote this comment if this is a **DANK MEME**. Downvote this comment if this is a **NORMIE MEME**.")
        comment.mod.distinguish(how='yes', sticky=True)
        comment.mod.approve()
        add_comment_db(comment,submission)


def check_scores():
    time.sleep(1)
    conn = sqlite3.connect('dankmemes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comments (comment_id, parent_post, reported)''')
    conn.commit()
    conn.close()

    reddit = praw.Reddit(client_id = '',
                        client_secret = '',
                        username = '',
                        user_agent = '',
                        password = '')


    user = reddit.redditor('keepdankmemesdank')
    for comment in user.comments.new(limit=400):
        comment_id = comment.id
        conn = sqlite3.connect('dankmemes.db')
        c = conn.cursor()s
        posts_db = c.execute('''SELECT * FROM comments WHERE comment_id=?''',[comment_id]).fetchone()
        if(posts_db):
            removed = posts_db[2]
            if(removed == "yes"):
                conn.close()
                continue
            else:
                conn.close()
                if(comment.score < -6):
                    if(comment.score < -20):
                        remove_post(comment, reddit)
                    report_post(comment, reddit)

        time.sleep(2)

def report_post(comment, reddit):
    conn = sqlite3.connect('dankmemes.db')
    c = conn.cursor()
    comment_id = comment.id
    posts_db = c.execute('''SELECT * FROM comments WHERE comment_id=?''',[comment_id]).fetchone()
    current = posts_db[1]
    post = reddit.submission(current)
    #msg_sub = reddit.subreddit('dankmemes')
    #post_link = post.shortlink
    #message_send = 'Mods, Please check this post, it reached the downvote threshold.  [Link](%s)' % post_link
    #msg_sub.message('Check Post', message_send)
    post.report("Not Dank.")
    c.execute('''UPDATE comments SET reported="yes" WHERE comment_id =?''', [comment_id])
    conn.commit()
    conn.close()

def remove_post(comment, reddit):
    conn = sqlite3.connect('dankmemes.db')
    c = conn.cursor()
    comment_id = comment.id
    posts_db = c.execute('''SELECT * FROM comments WHERE comment_id=?''',[comment_id]).fetchone()
    current = posts_db[1]
    post = reddit.submission(current)
    post.mod.remove()
    c.execute('''UPDATE comments SET reported="yes" WHERE comment_id =?''', [comment_id])
    conn.commit()
    conn.close()

def reporting_flaired():

    reddit = praw.Reddit(client_id = '',
                        client_secret = '',
                        username = '',
                        user_agent = '',
                        password = '')

def clearunmoderated():

    reddit = praw.Reddit(client_id = '',
                        client_secret = '',
                        username = '',
                        user_agent = '',
                        password = '')

    sub = reddit.subreddit('dankmemes')

    for submission in sub.mod.unmoderated(limit=None):
        if(submission.score < 10):
            ct = datetime.datetime.utcnow() - timedelta(hours=5)
            sub_t = datetime.datetime.fromtimestamp(submission.created_utc)
            diff = ct - sub_t
            hours = round(diff.total_seconds()/3600)
            if(hours > 1):
                submission.mod.remove()
            time.sleep(3)
        else:
            ct = datetime.datetime.utcnow() - timedelta(hours=5)
            sub_t = datetime.datetime.fromtimestamp(submission.created_utc)
            diff = ct - sub_t
            hours = round(diff.total_seconds()/3600)
            if(hours > 23):
                submission.mod.approve()
            time.sleep(3)


def clearcontroversial():

    reddit = praw.Reddit(client_id = '',
                        client_secret = '',
                        username = '',
                        user_agent = '',
                        password = '')

    sub = reddit.subreddit('dankmemes')

    for submission in sub.controversial('day', limit=None):

        if(submission.score < 10):
            ct = datetime.datetime.utcnow() - timedelta(hours=5)
            sub_t = datetime.datetime.fromtimestamp(submission.created_utc)
            diff = ct - sub_t
            hours = round(diff.total_seconds()/3600)
            if(hours > 1):
                submission.mod.remove()
            time.sleep(3)


while True:
    new_submissions()
    clearcontroversial()
    clearunmoderated()
    check_scores()
