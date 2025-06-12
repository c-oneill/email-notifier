from flask import Flask

import os
from dotenv import load_dotenv
import yagmail

# load environment variable
load_dotenv()

# Initialize Flask app
server = Flask(__name__)

# Initialize Yagmail SMTP client once
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)



@server.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@server.route("/test")
def send_test_email():
    try:
        yag.send(
            to=EMAIL_RECIPIENT,
            subject="Test",
            contents="Hello World"
        )
        return "<p>Email sent successfully!</p>"
    except Exception as e:
        return f"<p>Failed to send email: {e}</p>"