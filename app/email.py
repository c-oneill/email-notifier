import yagmail
from .config import EMAIL_USER, EMAIL_PASS, EMAIL_RECIPIENT

# Initialize Yagmail SMTP client once
yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)

def send_email(to, subject, content):
    try:
        yag.send(
            to=to,
            subject=subject,
            contents=content
        )
        return "<p>Email sent successfully!</p>"
    except Exception as e:
        return f"<p>Failed to send email: {e}</p>"
    

def send_test_email():
    return send_email(EMAIL_RECIPIENT, "Test", "Hello World")