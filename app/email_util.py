import yagmail
from .config import EMAIL_USER, EMAIL_PASS, EMAIL_RECIPIENT
from email_validator import validate_email, EmailNotValidError


# Initialize Yagmail SMTP client once
yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)

def send_email(to, subject, content):
    try:
        yag.send(
            to=to,
            subject=subject,
            contents=content
        )
    except Exception as e:
        printf("Email failed: {e}") # get context specific infor here for logger
        raise RuntimeException("Email failed: {e}") 

def send_test_email():
    return send_email(EMAIL_RECIPIENT, "Test", "Hello World")


# parse body from Twilio SMS webhook
def parse_message(body):
    
    # strip, parse by new lines
    lines = body.strip().splitlines(True)
    
    if len(lines) <= 0:
        raise ValueError("Expected at least 1 line: to, [subject], [body].")
    
    to = lines[0].strip()
    subject = ""
    contents = ""
    
    if len(lines) > 1:
        subject = lines[1].strip()
        
    if len(lines) > 2:
        contents = "".join(l for l in lines[2:])
    
    # email address validation
    try:
        result = validate_email(to)
        to = result.email  # Normalized and validated email
    except EmailNotValidError as e:
        print(f"Invalid email: {e}")
        raise ValueError("Invalid Email") from e
    
    return to, subject, contents


