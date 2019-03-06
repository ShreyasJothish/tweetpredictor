"""DB interface class is used to interact with DB"""
from .models import DB, User, Tweet
from .twitter import getuser, gettweets, gettwitterembedding
from sklearn.linear_model import LogisticRegression
import numpy as np

#def adduser(user_name):
#    """Add user and corresponding tweet_text into DB"""
#    try:
#        twitter_user = getuser(user_name)
#        tweets = gettweets(user_name)
#        db_user = User(id=twitter_user.id, name=twitter_user.screen_name, newest_tweet_id=tweets[0].id)
#
#        for tweet in tweets:
#            embedding = gettwitterembedding(tweet.full_text)
#            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
#            DB.session.add(db_tweet)
#            db_user.tweets.append(db_tweet)
#            
#        DB.session.add(db_user)
#        DB.session.commit()
#
#    except:
#        DB.session.rollback()
#        return False
#
#    return True

def add_or_update_user(username):
    """Add or update a user *and* their Tweets, error if no/private user."""
    try:
        import pdb; pdb.set_trace()
        twitter_user = getuser(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        # We want as many recent non-retweet/reply statuses as we can get
        tweets = gettweets(username, db_user.newest_tweet_id) 
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            # Get embedding for tweet, and store in db
            embedding = gettwitterembedding(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500],
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()


def predict_user(user1_name, user2_name, tweet_text, cache=None):
    """Determine and return which user is more likely to say a given Tweet."""
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression().fit(embeddings, labels)
    tweet_embedding = gettwitterembedding(tweet_text)
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
