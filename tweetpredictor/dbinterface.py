"""DB interface class is used to interact with DB"""
from .models import DB, User, Tweet
from .twitter import getuser, gettweets, gettwitterembedding

def adduser(user_name):
    """Add user and corresponding tweet_text into DB"""
    try:
        twitter_user = getuser(user_name)
        tweets = gettweets(user_name)
        db_user = User(id=twitter_user.id, name=twitter_user.screen_name, newest_tweet_id=tweets[0].id)

        for tweet in tweets:
            embedding = gettwitterembedding(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
            DB.session.add(db_tweet)
            db_user.tweets.append(db_tweet)
            
        DB.session.add(db_user)
        DB.session.commit()

    except:
        DB.session.rollback()
        return False

    return True

