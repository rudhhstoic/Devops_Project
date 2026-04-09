import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_email: str, symbol: str, analysis: dict):
    """Send stock analysis alert via Gmail SMTP."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("Email credentials not configured. Skipping email.")
        return

    sentiment = analysis.get("sentiment", "N/A")
    recommendation = analysis.get("recommendation", "N/A")

    emoji_map = {"Buy": "🚀", "Sell": "🔴", "Hold": "🟡"}
    emoji = emoji_map.get(recommendation, "📊")

    subject = f"Stock Alert: {symbol} - {recommendation} Signal {emoji}"

    body = f"""
🤖 AI Stock Advisor Alert
=========================

Stock: {symbol}

📊 Sentiment:      {sentiment}
💡 Recommendation: {recommendation}
🎯 Entry Point:    {analysis.get('entry_point', 'N/A')}

📝 Reason:
{analysis.get('reason', 'N/A')}

⚠️ Risks:
{analysis.get('risks', 'N/A')}

---
This is an automated alert from your AI Stock Advisor.
Not financial advice. Always do your own research.
    """.strip()

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())

    print(f"Email sent to {to_email} for {symbol}")
