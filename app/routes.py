from app import server
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
import app.email_util
from .decorators import validate_twilio_request


from .config import EMAIL_RECIPIENT

@server.route("/hello")
@server.route("/")
@server.route("/index")
def hello_world():
    return "<p>Hello, World!</p>"

@server.route("/test")
def send_test_email():
    return app.email_util.send_test_email()

@server.post("/msg")
def recieve_test_email():
    data = request.json
    return app.email_util.send_email(data["to"], data["subject"], data["content"])


@server.post("/sms")
@validate_twilio_request
def sms_reply():
    incoming_msg = request.form['Body']
    from_number = request.form['From']
    
    print(f"Message from {from_number}")
    
    # Create TwiML response
    resp = MessagingResponse()
    
    try:
        to, subject, contents = app.email_util.parse_message(incoming_msg)
        app.email_util.send_email(to, subject, contents)
        
        print(f"Email sent successfully. TO: {to}, SUBJECT: {subject}") 
        resp.message(f"Email sent: {subject}")
        
    except ValueError as ve:
        print(f"Input error: {ve}")
        resp.message(f"Input error: {ve}")
    except RuntimeError as re:
        print(f"Email error: {re}")
        resp.message(f"Email error: {re}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        resp.message(f"Unexpected error: {e}")
    
    return str(resp)


