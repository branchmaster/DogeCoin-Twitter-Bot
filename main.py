from config import get_tweepy_api
from researcher import DogeResearch
from publisher import DogePublisher

TERM_LIST = ["dogecoin", "doge", "dogearmy", "dogeday"]

def search_term_list(doge_research):
    list_tweet = {
            "certified" : [],
            "famous" : [],
            }

    for term in TERM_LIST:
        founded_tweets = doge_research.search(term)
        list_tweet['certified'].extend(founded_tweets['certified'])
        list_tweet['famous'].extend(founded_tweets['famous'])

    return list_tweet

if __name__ == "__main__":
    api = get_tweepy_api()
    list_tweet = search_term_list(DogeResearch(api))
    DogePublisher(api, list_tweet)
