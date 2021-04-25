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

    @classmethod
    def is_tweeted(cls, tweet):
        try:
            cls.get(cls.tweet_id == tweet.id_str)
            return True
        except cls.DoesNotExist:
            return False

db_tweet_record.create_tables([Tweets])
