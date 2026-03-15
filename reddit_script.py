import feedparser
from textblob import TextBlob
import smtplib
from email.message import EmailMessage
from fpdf import FPDF

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

# -------------------------
# Create PDF Report
# -------------------------

pdf=FPDF()
pdf.add_page()

pdf.set_font("Arial",size=16)
pdf.cell(200,10,txt="Daily Kindle Scribe Reddit Reviews",ln=True)

pdf.set_font("Arial",size=12)

pdf.cell(200,10,txt=" ",ln=True)
pdf.cell(200,10,txt="Positive Reviews:",ln=True)

for p in positive:
    pdf.multi_cell(0,8,p)

pdf.cell(200,10,txt=" ",ln=True)
pdf.cell(200,10,txt="Negative Reviews:",ln=True)

for n in negative:
    pdf.multi_cell(0,8,n)

pdf.output("reviews.pdf")

# -------------------------
# Send Email
# -------------------------

msg=EmailMessage()
msg['Subject']="Daily Kindle Scribe Reviews"
msg['From']="monishgit@gmail.com"
msg['To']="monishrm@amazon.com","qelavara@amazon.com"

msg.set_content("Please find the attached Reddit review report.")

with open("reviews.pdf","rb") as f:
    file_data=f.read()

msg.add_attachment(file_data,
                   maintype="application",
                   subtype="pdf",
                   filename="Reddit_Reviews_Report.pdf")

server=smtplib.SMTP_SSL("smtp.gmail.com",465)

server.login("monishgit@gmail.com","tloc bwwx zxwc oypg")

server.send_message(msg)

server.quit()

print("Mail with PDF report sent successfully")
