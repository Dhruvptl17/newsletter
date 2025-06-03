import requests
import smtplib
import schedule
import time
import os
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

NEWS_API_KEY = os.getenv("NEWSAPI_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # Comma-separated emails

def get_news():
    """
    Fetch news articles from NewsAPI based on tech/AI-related keywords.
    """
    target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=AI OR 'machine learning' OR technology&"
        f"from={target_date}&to={target_date}&"
        f"sortBy=popularity&language=en&"
        f"apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        print("Error: NewsAPI returned error status.")
        return []

    articles = data.get("articles", [])
    if not articles:
        print("No news articles found for the date.")
        return []

    summary = []
    for article in articles[:15]:  # Limit to top 15 articles
        title = article["title"]
        desc = article.get("description", "No description available.")
        link = article["url"]
        summary.append(
            f"<p><strong>{title}</strong><br>{desc}<br><a href='{link}'>Read more</a></p>"
        )

    return summary

def send_email(news_items):
    """
    Send the compiled news items via email using Gmail SMTP.
    """
    digest_date = (datetime.now() - timedelta(days=1)).strftime('%B %d, %Y')
    subject = f"AI & Tech News Digest – {digest_date}"

    html_body = f"""
    <html>
        <body>
            <h2>Top AI/Tech News for {digest_date}</h2>
            {''.join(news_items)}
            <hr>
            <p style='font-size:12px;'>Generated automatically by your Python script.</p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(EMAIL_RECEIVER.split(","))
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(
                EMAIL_SENDER,
                EMAIL_RECEIVER.split(","),
                msg.as_string()
            )
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

def daily_job():
    """
    Main job that gets news and sends the email.
    """
    news_items = get_news()
    if news_items:
        send_email(news_items)
    else:
        print("No news to send today.")

# Run now for testing
daily_job()

# Uncomment below to enable daily 6:00 AM automation
# schedule.every().day.at("06:00").do(daily_job)
# while True:
#     schedule.run_pending()
#     time.sleep(60)
