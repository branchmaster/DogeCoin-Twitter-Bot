import datetime

class DogeResearch:
    """
    Search for tweet related to given keywords.
    Get only tweet published by certified account, or with
    important social activity, with metrics above LIKES, RETWEETS
    and COMMENTS.
    """
    #Expected number of likes, retweets, should indicate tweet fame
    LIKES = 150
    RETWEETS = 150
    COMMENTS = 150
    HOURS_PREVIEW = 2

    #Config variables
    LANG="en"

    def __init__(self, api):
        #Login to twitter
        self._api = api

    def search(self, keyword):
        """
        Retrieve list of tweet related to given keyword.
        """
        famous_tweets = self._famous_search(keyword)
        certified_tweets = self._certified_search(keyword)

        return {"certified" : certified_tweets,
                "famous" : famous_tweets}

    def _query(self, keyword, extra_parameters):
        """
        Query for all api request, to add default parameters
        on each query.
        """
        #Prepare entire query parameters
        default_parameters = [
                f"{keyword} OR #{keyword}",
                "-filter:retweets",
                ]
        query = " ".join(default_parameters + extra_parameters)

        #Perform the query
        tweet_list = self._api.search(query, lang=self.LANG,
                result_type="recent")

        #Filter the query
        return list(filter(self._date_filter, tweet_list))

    def _famous_search(self, keyword):
        """
        Query search of tweet with good social metrics,
        using LIKES, COMMENTS and RETWEET limitation.
        """
        #Set social metrics, retrieve post having one
        #or more of this metrics using OR operator
        social_metrics = [
                f"min_replies:{self.COMMENTS}",
                f"min_faves:{self.LIKES}",
                f"min_retweets:{self.RETWEETS}",
                ]
        social_metrics_query = " OR ".join(social_metrics)

        query_parameters = [
                social_metrics_query,
                f"-filter:verified",
                ]
        return self._query(keyword, query_parameters)

    def _certified_search(self, keyword):
        """
        Query search of tweet posted by certified account only.
        """
        query_parameters = [
                "filter:verified",
                ]
        return self._query(keyword, query_parameters)

    def _date_filter(self, tweet):
        """
        Filter function, verify if tweet have been posted in range
        inferior to HOURS_PREVIEW.
        """
        hours_limit = datetime.timedelta(hours=self.HOURS_PREVIEW)
        release_since = datetime.datetime.utcnow() - tweet.created_at

        return release_since <= hours_limit
