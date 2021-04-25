class TwitterResearcher:
    """
    Interface to search list of tweet related to given keyword.
    Enable a query configuration, see self.search for available
    parameters.
    """
    #Config variables
    LANG="en"

    def __init__(self, api):
        #Login to twitter
        self._api = api

    def search(self, keyword, certified=None, tweet_filter=None,
            min_faves=None, min_retweets=None, min_replies=None):
        """
        Search for list of tweet for a given keyword.

        Available parameters:
        @keyword:                       Keyword to search for
        @certified: [True|False|None]   Get only or no certified account,
                                        None won't care about.
        @tweet_filter:                  (Work in progress)
        @min_faves:                     Minimum number of likes
        @min_retweets:                  Minimum number of retweets
        @min_replies:                   Minimum number of replies
        """
        parameters = self._prepare_parameters(
                keyword=keyword, certified=certified,
                min_faves=min_faves, min_retweets=min_retweets,
                min_replies=min_replies
                )

        query = " ".join(parameters)

        #Perform the query using Twitter API
        tweet_list = self._api.search(query, lang=self.LANG,
                result_type="recent")

        #Apply filters on the list of tweet.
        final_tweet_list = filter(tweet_filter, tweet_list)

        return list(final_tweet_list)

    def multiple_search(self, keyword_list, *args, **kwargs):
        """
        Search for multiple keyword at once, using same parameters
        for each query.
        """
        tweet_list = []

        for keyword in keyword_list:
            tweet_list += self.search(keyword, *args, **kwargs)
        return tweet_list

    def _prepare_parameters(self, keyword, certified, 
            min_faves, min_retweets, min_replies):
        """
        Create all query parameters according to the configuration.
        """
        query_parameters = []

        #Use each helpers to fill parameters
        query_parameters += self._certified_parameters(certified)
        query_parameters += self._minimal_parameters(min_faves,
                min_retweets, min_replies)
        query_parameters += self._default_parameters()

        #Finally set up keyword argument
        keyword_parameter = f"{keyword} OR #{keyword}"
        query_parameters.append(keyword_parameter)

        return query_parameters

    @staticmethod
    def _certified_parameters(certified):
        """
        Enable/disable search with certified account only.

        @certified: accept True, False or None.

        True or False will enable or disable the search of
        certified account.
        None will allow both, normal search.
        """
        parameters = []
        if certified is not None:
            parameters.append("filter:verified")
        if certified is False:
            parameters[0] = "-" + parameters[0]
        return parameters

    @staticmethod
    def _minimal_parameters(min_faves, min_retweets,
            min_replies):
        """
        Create parameters for minimum like, retweets and replies.

        If enabled, query will format the entire set with OR operator.
        """
        parameters = []

        #Format string for each type, like "min_retweets:15"
        for minimal_type in {"faves", "retweets", "replies"}:
            minimal_type = "min_" + minimal_type
            minimal_value = locals()[minimal_type]

            if minimal_value is not None:
                minimal_argument = f"{minimal_type}:{minimal_value}"
                parameters.append(minimal_argument)

        #Create single string with all minimal using OR operator.
        if len(parameters) > 0:
            parameters = [" OR ".join(parameters)]

        return parameters

    @staticmethod
    def _default_parameters():
        """
        Parameters by defaults, applied to every query.
        """
        parameters = [
                "-filter:retweets",
                ]
        return parameters
