"""Main application and routing logic for tweetpredictor."""
from flask import Flask
from .models import DB
from .dbinterface import * 

app = Flask(__name__) 
def create_app():
    """Create and configure an instance of the Flask application."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to tweetpredictor!'

    return app

@app.route('/getalluser')
def getalluser():
    """Returns information about the Users in DB"""
    return getalluserinfo()

@app.route('/add/<user_name>/<tweet_text>')
def add(user_name, tweet_text):
    """Create/add user and corresponding tweet_text"""
    ret = adduserandtweet(user_name, tweet_text)
    
    if ret == True:
        return "Add successful"
    
    return "Add failure"
