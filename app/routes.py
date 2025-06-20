from app import server
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
import app.email
from .decorators import validate_twilio_request


@server.route("/hello")
@server.route("/")
@server.route("/index")
def hello_world():
    return "<p>Hello, World!</p>"

@server.route("/test")
def send_test_email():
    return app.email.send_test_email()

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