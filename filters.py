import os
import datetime
from record import Tweets

class TwitterFilter:
    """
    Filter manager to remove unexpected tweet.
    Will be applied to each tweet when receving
    a new list.
    """
    #Maximum time since tweet posted
    HOURS_PREVIEW = 2

    DEFAULT_FILTERS = [
            "hours_limit",
            "user_ban",
            "posted_tweet",
            ]

    def __init__(self, filter_list=[], ban_file="ban_user"):
        self.ban_list = self._config_ban(ban_file)
        self.filter_list = filter_list

    @staticmethod
    def _config_ban(ban_file):
        """
        Retrieve list of user specified in a ban file.
        Ban file must have a single username by row.

        Exemple:
        user_to_ban_1
        user_to_ban_2
        etc.
        """
        banned_users = []
        if not os.path.exists(ban_file):
            return banned_users

        with open(ban_file) as ban_file_stream:
            ban_list = ban_file_stream.readlines()

        #Clean up user list
        ban_list = map(str.strip, ban_list)
        return list(ban_list)

    def hours_limit(self, tweet):
        """
        Filter function, verify if tweet have been posted in range
        inferior to HOURS_PREVIEW.
        """
        hours_limit = datetime.timedelta(hours=self.HOURS_PREVIEW)
        release_since = datetime.datetime.utcnow() - tweet.created_at

        return release_since <= hours_limit

    def user_ban(self, tweet):
        """
        Control if the user isn't black listed.
        """
        tweet_user = tweet.author.screen_name
        return tweet_user not in self.ban_list

    def posted_tweet(self, tweet):
        """
        Remove already posted tweet.
        """
        return not Tweets.is_tweeted(tweet)

    def __call__(self, tweet):
        """
        Apply each configured filters. Return False if any of
        those filter is False.
        """
        #Get all configured filters
        applied_filters = self.DEFAULT_FILTERS + self.filter_list

        #Apply each filter to the tweet
        for filter_method_name in applied_filters:
            filter_method = getattr(self, filter_method_name)
            if filter_method(tweet) is False:
                return False
        return True
