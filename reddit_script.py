import feedparser
from textblob import TextBlob
import smtplib
from email.message import EmailMessage

rss_url="https://www.reddit.com/r/kindlescribe/.rss"

feed=feedparser.parse(rss_url)

positive=[]
negative=[]

for post in feed.entries[:20]:

    title=post.title
    sentiment=TextBlob(title).sentiment.polarity

    if sentiment>0:
        positive.append(title)
    else:
        negative.append(title)

body="Positive Reviews:\n\n"

for p in positive:
    body+=p+"\n"

body+="\n\nNegative Reviews:\n\n"

for n in negative:
    body+=n+"\n"

msg=EmailMessage()
msg['Subject']="Daily Kindle Scribe Reviews"
msg['From']="monishgit@gmail.com"
msg['To']="monishrm@amazon.com"

msg.set_content(body)

server=smtplib.SMTP_SSL("smtp.gmail.com",465)
server.login("monishgit@gmail.com","tloc bwwx zxwc oypg")

server.send_message(msg)
server.quit()
