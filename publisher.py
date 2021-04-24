from datetime import datetime
import peewee

db_tweet_record = peewee.SqliteDatabase("tweets.db")

class Tweets(peewee.Model):
    """
    SQL table to store list of published tweet. Let avoid
    posting twice the same tweet.
    """
    tweet_id = peewee.CharField(unique=True)

    class Meta:
        database = db_tweet_record

db_tweet_record.create_tables([Tweets])

class DogePublisher:
    """
    Manage publication of tweet list related to dogecoin.

    Create thread to display all tweet in the same place.
    """
    def __init__(self, api, requested_tweets):
        self._api = api

        self._remove_posted_tweets(requested_tweets)
        #Avoid post if no tweet founded
        if not any(requested_tweets.values()):
            exit()

        self.post_thread(requested_tweets)

    def _remove_posted_tweets(self, requested_tweets):
        """
        Remove already posted tweet stored in Tweets sql table.
        """
        for category in requested_tweets:
            unsended_tweets = [tweet for tweet in requested_tweets[category]
                    if not self._is_tweeted(tweet)]
            requested_tweets[category] = unsended_tweets

    def post_thread(self, requested_tweets):
        """
        Post the entire thread on twitter profil
        linked to the program.
        """
        now = datetime.utcnow().strftime("%m/%d %H:%M UTC")

        message = f"Update {now}\n\n"
        message += "Track #DogeCoin related keywords/hashtags\n" + \
        "Display list of tweet from certified account or with social activity.\n\n" + \
        "To get all threads, perform search using 'Update (from:DogeNewsBot1)'"

        last_id = self._api.update_status(message).id

        last_id = self.post_tweet_list(requested_tweets['certified'],
                intro_sentence="Certified Account ✅",
                previous_id_tweet=last_id)

        self.post_tweet_list(requested_tweets['famous'],
                intro_sentence="Active tweet 🚀",
                previous_id_tweet=last_id)

    @staticmethod
    def _is_tweeted(tweet_id):
        try:
            Tweets.get(Tweets.tweet_id == tweet_id)
            return True
        except Tweets.DoesNotExist:
            return False

    @staticmethod
    def _store_tweet(tweet_id):
        Tweets.create(tweet_id=tweet_id).save()

    def post_tweet_list(self, tweet_list, intro_sentence, \
            previous_id_tweet):
        """
        Post a list of tweet in a threded tweet.
        Add an introduction sentance in the first tweet.
        """
        for tweet in tweet_list:
            if self._is_tweeted(tweet.id_str):
                continue

            text = intro_sentence + "\n"
            
            tweet_url = "https://twitter.com/{}/status/{}".format(
                    tweet.author.id,
                    tweet.id
                    )

            text += tweet_url
            
            new_tweet = self._api.update_status(text,
                    in_reply_to_status_id=previous_id_tweet,
                    auto_populate_reply_metadata=True)

            previous_id_tweet = new_tweet.id
            self._store_tweet(tweet.id_str)

        return previous_id_tweet
