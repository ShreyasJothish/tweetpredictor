"""Main application and routing logic for tweetpredictor."""
from flask import Flask, render_template, request
from .models import DB, User
from .dbinterface import adduser 

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__) 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = 'debug'
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])

    @app.route('/add/<user_name>')
    def add(user_name):
        """Add user and corresponding tweet_text into DB"""
        ret = adduser(user_name)
    
        if ret == True:
            users = User.query.all()
            return render_template('base.html', title='Home', users=users)
    
        return f"Adding {user_name} failed"
    
    @app.route('/user/<user_name>')
    def gettweets(user_name):
        """Returns tweets specific to a user"""
        user = User.query.filter(User.name == user_name).first()
        return render_template('tweet.html', title='Tweets', user=user)

    return app

