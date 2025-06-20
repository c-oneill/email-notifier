import os
from dotenv import load_dotenv

# load environment variable
load_dotenv()

EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")