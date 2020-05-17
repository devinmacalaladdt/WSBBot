#!/usr/bin/python
import praw
import re
import sys
import time
from datetime import datetime, timezone

reddit = praw.Reddit('bot1')
tickers = sys.argv[1:]
f=open("res.txt", "w", encoding="utf-8")
print(tickers)
subreddit = reddit.subreddit("wallstreetbets")
for submission in subreddit.hot(limit=1):
    if submission.stickied:
        submission.comments.replace_more(limit=30)
        f.write("***************\n"+(datetime.utcfromtimestamp(float(submission.created))).strftime('%m/%d/%Y')+"\n***************\n")
        for comment in submission.comments:
            for t in tickers:
                if re.search(t, comment.body, re.IGNORECASE):
                    f.write(t+"\n")
                    f.write("["+(datetime.utcfromtimestamp(float(comment.created_utc))).strftime('%m/%d/%Y---%H:%M')+"]\n"+comment.body+"\n")
                    for reply in comment.replies:
                        f.write("\t->"+reply.body+"\n")
                    f.write("====================================================\n")
                    break
f.close()