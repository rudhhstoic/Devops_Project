import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_email: str, symbol: str, analysis: dict):
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("Email credentials not configured.")
        return

    sentiment = analysis.get("sentiment", "N/A")
    recommendation = analysis.get("recommendation", "N/A")
    emoji_map = {"Buy": "🚀", "Sell": "🔴", "Hold": "🟡"}
    emoji = emoji_map.get(recommendation, "📊")

    subject = f"Stock Alert: {symbol} - {recommendation} Signal {emoji}"
    body = f"""
AI Stock Advisor Alert
======================
Stock: {symbol}
Sentiment:      {sentiment}
Recommendation: {recommendation}
Entry Point:    {analysis.get('entry_point', 'N/A')}

Reason:
{analysis.get('reason', 'N/A')}

Risks:
{analysis.get('risks', 'N/A')}

---
Not financial advice. Always do your own research.
    """.strip()

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Use STARTTLS on port 587 instead of SSL on 465 — more reliable
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
            server.quit()
        print(f"✅ Email sent to {to_email} for {symbol}")
    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail auth failed — check App Password in .env")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
    except Exception as e:
        print(f"❌ Email failed: {e}")