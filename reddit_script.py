import feedparser
from textblob import TextBlob
import smtplib
from email.message import EmailMessage
from fpdf import FPDF
import os

# -------------------------
# Fetch Reddit Data
# -------------------------
rss_url = "https://www.reddit.com/r/kindlescribe/.rss"

feed = feedparser.parse(
    rss_url,
    request_headers={'User-Agent': 'Mozilla/5.0'}
)

positive = []
negative = []

for post in feed.entries[:20]:
    title = post.title
    link = post.link
    sentiment = TextBlob(title).sentiment.polarity

    if sentiment > 0.1:
        positive.append((title, link))
    elif sentiment < -0.1:
        negative.append((title, link))

# -------------------------
# Create PDF with Hyperlinks
# -------------------------
pdf = FPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Daily Kindle Scribe Reddit Reviews", ln=True)

pdf.ln(5)

# Positive Section
pdf.set_font("Arial", "B", 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 10, "Positive Reviews:", ln=True)

pdf.set_font("Arial", "", 11)

for title, link in positive:
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, title.encode('latin-1','replace').decode('latin-1'))
    
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Arial", "U", 11)
    pdf.cell(0, 8, "Open Post", ln=True, link=link)
    
    pdf.ln(3)
    pdf.set_font("Arial", "", 11)

# Negative Section
pdf.ln(5)
pdf.set_font("Arial", "B", 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 10, "Negative Reviews:", ln=True)

pdf.set_font("Arial", "", 11)

for title, link in negative:
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, title.encode('latin-1','replace').decode('latin-1'))
    
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Arial", "U", 11)
    pdf.cell(0, 8, "Open Post", ln=True, link=link)
    
    pdf.ln(3)
    pdf.set_font("Arial", "", 11)

pdf.output("Reddit_Reviews_Report.pdf")

# -------------------------
# Send Email
# -------------------------
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASS")

msg = EmailMessage()
msg['Subject'] = "Daily Kindle Scribe Reviews"
msg['From'] = EMAIL
msg['To'] = "monishrm@amazon.com, qelavara@amazon.com, rdkavith@amazon.com"

msg.set_content("Please find the attached Reddit review report with clickable links.")

with open("Reddit_Reviews_Report.pdf", "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="pdf",
        filename="Reddit_Reviews_Report.pdf"
    )

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL, PASSWORD)

server.send_message(msg)
server.quit()

print("✅ Mail with PDF report sent successfully 🚀")
