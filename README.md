# email-notifier

As is now: text a fixed phone number, to send an email. Or leave a voicemail, get transciprion in a fixed email inbox.

text:
<recipient email>
<subject>
<multiline body>

SETUP:

1. setup gmail account
	-setup a new email or use an old one
	-get an app password: https://support.google.com/mail/answer/185833?hl=en

2. setup twilio account: https://login.twilio.com/u/signup
	-free trial ok
	-grab twilio account SID and Twilio Authorization token from the console
		Admin > Account Management > Keys and Credentials > API Keys and tokens
	-buy new number with SMS capabilities (Phone Numbers > Manage > Buy a number)

3. use template.env to create your own .env file

4. Deploy on Render
	-hobby acct ok
	-New + > Web Service
	-connect with GitHub repo

	-deploying instance: (free instance OK)
	Environment: Python
	Build command: pip install -r requirements.txt
	Start command: gunicorn app:server --bind 0.0.0.0:10000

	Add .env as secret file

5. Configure SMS webhook with Twilio
	-use the URL from the Render dashboard
	-Phone Numbers > Manage > Active Numbers > Configure > Messaging Configuration > A message comes in
		Webhook, POST, URL: https://<your project>.onrender.com/sms
	
6. Try it out! 
	-Send a text to the twilio bought phone number above 
	-Leave a voicemail to the twilio bought phone number above 
	-check gmail inbox
