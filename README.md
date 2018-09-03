# Infographics Moderator Toolbox

This is a set of scripts adapted from /r/dankmemes to help moderate the /r/infographics subreddit in a more efficient fashion.

## Set up

Make sure that `praw` is installed. You can install this with:
```bash
pip install praw
```

The toolbox uses python 3. 

Some of the scripts also make use of a local sqlite3 database, and interact with it using the STL sqlite library. 

To get started, make a file called `settings.txt` in the same directory as CommonUtils.py.

This file should have 4 lines, formatted as so:

```text
App-ID
App-Secret
Moderator Username
Moderator Password
```

The App-ID and App-Secret should be created by the moderator that you are using the username/password of on lines 3 and 4. 

You can get an Id and Secret by clicking "Create an app" on this [page](https://www.reddit.com/prefs/apps/).

You should then be able to run any of the scripts with `python script.py`.