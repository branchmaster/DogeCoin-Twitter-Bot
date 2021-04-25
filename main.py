from config import get_tweepy_api
from researcher import TwitterResearcher
from publisher import TwitterPublisher
from filters import TwitterFilter

TERM_LIST = ["dogecoin", "doge", "dogearmy", "dogeday"]

def bot_routine(searcher, publisher):
    """
    Perform bot routine, research and post list of tweet.

    Prepare mutliple list to be posted at once in a single thread.
    """
    #Search tweets from certified account
    certified_tweets = searcher.multiple_search(TERM_LIST,
            certified=True, tweet_filter=TwitterFilter())
    publisher.store_tweet_list("Certified Account ✅", certified_tweets)

    #Search tweets with some social activity, with
    #minimal likes, retweets or replies.
    low_limit = 150
    active_tweets = searcher.multiple_search(TERM_LIST, certified=False,
            tweet_filter=TwitterFilter(), min_faves=low_limit,
            min_retweets=low_limit, min_replies=low_limit)
    publisher.store_tweet_list("Active tweet 🚀", active_tweets)

    #Publish each stored list on Twitter as a single thread.
    publisher.post_thread()

if __name__ == "__main__":
    api = get_tweepy_api()
    bot_routine(TwitterResearcher(api), TwitterPublisher(api))
