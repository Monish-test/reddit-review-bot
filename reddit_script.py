//script

import praw
from textblob import TextBlob
import smtplib
from email.message import EmailMessage
import os

reddit = praw.Reddit(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    user_agent="review_script"
)

subreddit = reddit.subreddit("kindlescribe")

positive=[]
negative=[]

for post in subreddit.new(limit=30):

    text=post.title
    score=TextBlob(text).sentiment.polarity

    if score>0:
        positive.append(text)
    else:
        negative.append(text)

body="Positive Reviews:\n\n"

for p in positive:
    body+=p+"\n"

body+="\n\nNegative Reviews:\n\n"

for n in negative:
    body+=n+"\n"

msg=EmailMessage()
msg['Subject']="Daily Kindle Scribe Reviews"
msg['From']=os.environ['EMAIL']
msg['To']=os.environ['EMAIL']

msg.set_content(body)

server=smtplib.SMTP_SSL("smtp.gmail.com",465)
server.login(os.environ['EMAIL'],os.environ['EMAIL_PASSWORD'])
server.send_message(msg)
server.quit()
