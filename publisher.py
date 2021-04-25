from datetime import datetime
from record import Tweets

class TwitterPublisher:
    """
    Manage publication of tweet list related to dogecoin.

    Create thread to display all tweet in the same place.
    """
    def __init__(self, api):
        self._api = api
        self.registered_lists = []

        #Always Keep last tweet id, reply is used to create thread
        self._last_tweet_id = None

    def store_tweet_list(self, intro_sentence, tweet_list):
        """
        Store a single list of tweet who will be displayed in the thread.
        Associate each list with a sentence display with each tweet
        of this list.
        """
        if tweet_list:
            self.registered_lists.append((intro_sentence, tweet_list))

    def post_thread(self):
        """
        Post the entire thread on twitter profil
        linked to the program.
        """
        #Avoid post if no tweet founded
        if not self.registered_lists:
            return None

        #Post introduction message, first tweet of the thread
        self._last_tweet_id = self._api.update_status(self._intro_message).id

        #Post all stored list one by one
        for intro_sentence, tweet_list in self.registered_lists:
            self._post_tweet_list(tweet_list, intro_sentence)

    @property
    def _intro_message(self):
        """
        Format the introduction tweet, first tweet of the thread.
        """
        now = datetime.utcnow().strftime("%m/%d %H:%M UTC")

        message = f"Update {now}\n\n"
        message += "Track #DogeCoin related keywords/hashtags\n" + \
        "Display list of tweet from certified account or with social activity.\n\n"
        message += "To get all threads, perform search using 'Update (from:{})'".\
                format(self._api.me().screen_name)
        return message

    def _post_tweet_list(self, tweet_list, intro_sentence):
        """
        Post a list of tweet in a threded tweet.
        Add an introduction sentance in the first tweet.
        """
        for tweet in tweet_list:
            if Tweets.is_tweeted(tweet):
                continue

            tweet_url = "https://twitter.com/{}/status/{}".format(
                    tweet.author.id,
                    tweet.id
                    )

            text = intro_sentence + "\n"
            text += tweet_url
            
            new_tweet = self._api.update_status(text,
                    in_reply_to_status_id=self._last_tweet_id,
                    auto_populate_reply_metadata=True)

            self._last_tweet_id = new_tweet.id

            #Store tweet id in sql database
            Tweets.store_tweet(tweet)
