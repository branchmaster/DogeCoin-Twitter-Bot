import tweepy
import os

def get_tweepy_api():
    """
    Logging to twitter API using user tokens.
    Credential must be storred in environnement variables, using .env file.
    """
    auth = tweepy.OAuthHandler(
            os.environ["API_KEY"],
            os.environ["API_SECRET"]
            )
    auth.set_access_token(
            os.environ["API_ACCESS_TOKEN"],
            os.environ["API_SECRET_TOKEN"]
            )

    return tweepy.API(auth)
