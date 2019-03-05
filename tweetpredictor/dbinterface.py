"""DB interface class is used to interact with DB"""
from .models import DB, User, Tweet

def getalluserinfo():
    """Returns information about the Users in DB"""
    output = ""
    allusers = User.query.all()
    for user in allusers:
        name = user.name
        output += name + "\n"
        tweets = user.tweets
        for tweet in tweets:
            output += tweet.text + "\n"

    return output

def adduserandtweet(user_name, tweet_text):
    """Create/add user and corresponding tweet_text"""
    user = User.query.filter(User.name == user_name).first()
    tweet = Tweet(text=tweet_text)
    print(f"coming here {user_name}:{tweet_text}") 
    print(user)
    try:
        if user:
            print("inside if")
            user.tweets.append(tweet)
            
            DB.session.add(user)
            DB.session.add(tweet)

        else:
            print("inside else")
            newuser = User(name=user_name)
            newuser.tweets.append(tweet)

            DB.session.add(newuser)
            DB.session.add(tweet)
        
        print("before commit")
        DB.session.commit()
    
    except:
        DB.session.rollback()
        return False

    return True

