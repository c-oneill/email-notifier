from app import server
from flask import request, current_app, url_for
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import app.email_util
from .decorators import validate_twilio_request


from .config import EMAIL_RECIPIENT, TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN

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
    return app.email_util.send_email(data["To"], data["From"], data["Subject"], data["Content"])


'''
Handles Twilio SMS webhook
'''
@server.post("/sms")
@validate_twilio_request
def sms_response():
    incoming_msg = request.form['Body']
    from_number = request.form['From']
    
    print(f"Message from {from_number}")
    
    # Create TwiML response
    resp = MessagingResponse()
    
    try:
        to, subject, contents = app.email_util.parse_message(incoming_msg)
        app.email_util.send_email(to, from_number, subject, contents)
        
        print(f"Email sent successfully. TO: {to}, FROM: {number_from}, SUBJECT: {subject}") 
        resp.message(f"Email sent: {subject}")
        
    except ValueError as ve:
        print(f"Input error: {ve}")
        resp.message("Invalid input format.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        resp.message("Sorry, something went wrong. Please try again later.")
    
    return str(resp)


'''
Handles Twilio Voice webhook
Returns TwiML which prompts the caller to record a message
'''
@server.post("/record")
@validate_twilio_request
def record_call():

    # Start TwiML response
    response = VoiceResponse()

    # Use <Say> to give the caller some instructions
    response.say('Hello. Please leave a message after the beep.')

    # Use <Record> to record the caller's message, set to transcribe
    callbackurl = url_for('transcription_callback', _external=True)
    response.record(transcribe="true", transcribeCallback=f"{callbackurl}")

    # End the call with <Hangup>
    response.hangup()

    return str(response)    
      
'''
Handles Twilio Transcription Callback webhook
Retrives transcription
'''
@server.post("/transcription")
@validate_twilio_request
def transcription_response():

    contents = request.form['TranscriptionText']
    from_number = request.form['From']
    transcription_sid = request.form['TranscriptionSid']
    status = request.form['TranscriptionStatus']
    
    if status == "failed":
        # possibly empty transcription text
        print(f"Transcription failed for recording from {from_number}")
    else:
        print(f"Transcription succeeded for recording from {from_number}")
        
    try:
        to = EMAIL_RECIPIENT
        subject = "VOICE to TEXT"
        
        # send email
        app.email_util.send_email(to, from_number, subject, contents)
        print(f"Email sent successfully. TO: {to}, FROM: {from_number}, SUBJECT: {subject}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")

    
    # if DEBUG is false, delete transcription
    if not current_app.debug:
        client = Client(TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN)
        client.transcriptions(transcription_sid).delete()
        print("Transcription deleted for recording from {from_number}.")
        # todo: error handling here?
        # todo: delete recording?
    
    return "", 204 # no content needed
    

