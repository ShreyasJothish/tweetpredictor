"""Main application and routing logic for tweetpredictor."""
from flask import Flask, render_template, request
from .models import DB, User
from .appimpl import add_or_update_user, predict_user

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__) 
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

    #@app.route('/add/<user_name>')
    #def add(user_name):
    #    """Add user and corresponding tweet_text into DB"""
    #    ret = adduser(user_name)
    #
    #    if ret == True:
    #        users = User.query.all()
    #        return render_template('base.html', title='Home', users=users)
    #
    #    return f"Adding {user_name} failed"
    
    #@app.route('/gettweets/<user_name>')
    #def gettweets(user_name):
    #    """Returns tweets specific to a user"""
    #    user = User.query.filter(User.name == user_name).first()
    #    return render_template('tweet.html', title='Tweets', user=user)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        message=''
        #import pdb; pdb.set_traces()
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)


    @app.route('/compare', methods=['POST'])
    def compare():
        user1, user2 = request.values['user1'], request.values['user2']
        if user1 == user2:
            return 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'])
            return user1 if prediction else user2
    
    return app

