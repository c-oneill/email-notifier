import os
from dotenv import load_dotenv
import yagmail
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# load environment variable
load_dotenv()

# Initialize Flask app
server = Flask(__name__)

# Initialize Yagmail SMTP client once
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)


@server.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

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


@server.route("/test")
def send_test_email():
    return send_email(EMAIL_RECIPIENT, "Test", "Hello World")


@server.post("/msg")
def recieve_test_email():
    data = request.json
    return send_email(data["to"], data["subject"], data["content"])


@server.post("/sms")
@validate_twilio_request
def sms_reply():
    incoming_msg = request.form['Body']
    from_number = request.form['From']
    
    print(f"Message from {from_number}: {incoming_msg}")
    print(send_email(EMAIL_RECIPIENT, f"Twilio/Render Test, from {from_number}", incoming_msg))

    # Create TwiML response
    resp = MessagingResponse()
    resp.message(f"You said: {incoming_msg}")
    return str(resp)



