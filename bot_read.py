#!/usr/bin/python
import praw
import re
import sys
import time
from datetime import datetime, timezone
from collections import OrderedDict

reddit = praw.Reddit('bot1')
tickers = sys.argv[1:]
pop_tickers = OrderedDict()
f=open("res.txt", "w", encoding="utf-8")
subreddit = reddit.subreddit("wallstreetbets")
for submission in subreddit.hot(limit=1):
    if submission.stickied:
        submission.comments.replace_more(limit=100)
        f.write("***************\n"+(datetime.utcfromtimestamp(float(submission.created))).strftime('%m/%d/%Y')+"\n***************\n")
        for comment in submission.comments:
            words = re.split('[ \t\n]',comment.body)
            found = False
            for word in words:
                if len(word)<=4 and word.isupper():
                    if found is False and word in tickers:
                        f.write(word+"\n")
                        f.write("["+(datetime.utcfromtimestamp(float(comment.created_utc))).strftime('%m/%d/%Y---%H:%M')+"]\n"+comment.body+"\n")
                        for reply in comment.replies:
                            f.write("\t->"+reply.body+"\n")
                        f.write("====================================================\n")
                        found = True
                    if word in pop_tickers:
                        pop_tickers[word] += 1
                    else:
                        pop_tickers[word] = 1

f.write("TOP TICKERS:\n")
for tick,mentions in pop_tickers.items():
    f.write(tick+"\tmentions: "+str(mentions)+"\n")
f.close()