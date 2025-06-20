from flask import Flask, request

# Initialize Flask app
server = Flask(__name__)

# avoids circular imports
from app import routes