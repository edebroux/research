from tweepy import Status
from typing import Dict, List, Set
# from twitter_fire_scraper.text_classifier import classifier
from util import flatten_status_dict
from twitter_fire_scraper.twitter import TwitterAuthentication
import tweepy
import os
from pprint import pprint

class Scraper():

    def __init__(self, twitter_authentication=None):
        # type: (Scraper, TwitterAuthentication) -> None

        # They did not pass in any authentication. Attempt to auto-detect it.
        if not twitter_authentication:
            self.twitter_authentication = TwitterAuthentication.autodetect_twitter_auth()
        else:  # They passed us a TwitterAuthentication object
            self.twitter_authentication = twitter_authentication

        # Tweepy API object. Can make API calls.
        self.api = tweepy.API(self.twitter_authentication.oauth_handler,
                              wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # Default amount of tweets to retrieve.
        self.default_count = 10

        # Default accounts to scrape.
        # self.accounts = accounts in data/TwitterAccounts.yml

    def scrape_terms(self, terms, count=None, geocode=None):
        # type: (Scraper, Set[str], int, str) -> Dict[str, List[Status]]
        """
        Term-scraping method. Can scrape a set of terms.

        A term is either a hashtag or a piece of text.

        :param geocode: Geographical area to search in. Can be blank.
        :param terms:  List of terms to search for.
        :param count: Maximum tweets to return per search term.
        :return: A dictionary containing {'search-term': List[Status]} pairs.
        """

        if not count:
            count = self.default_count

        results = {}  # type: Dict[str, List[Status]]

        # For each search term,
        for search_term in terms:

            # Make a cursor that can get tweets.
            cursor = tweepy.Cursor(self.api.search, q=search_term, geocode=geocode)

            # For each result of a search term,
            for status in cursor.items(count):  # type: Status

                if search_term not in results:
                    results[search_term] = list()

                # Add the status to a particular search term.
                results[search_term].append(status)

        return results

    def scrape_accounts(self, accounts, count=None):
        # type: (Scraper, Set[str], int) -> Dict[str, List[Status]]
        """
        Account-scraping method. Can scrape a set of accounts.

        An account is either a screenname or @screenname, i.e. both 'Dude123' and '@Dude123' are valid.

        :param accounts: List of accounts to search in.
        :param count: Maximum tweets to return per account.
        :return: A dictionary containing {'@Dude123': List[Status]} pairs.
        """

        if not count:
            count = self.default_count

        all_the_tweets = {}
        for i in accounts:
            new_tweets = self.api.user_timeline(screen_name=i, count=count)
            all_the_tweets[i] = new_tweets

        return flatten_status_dict(all_the_tweets)
        # return all_the_tweets

        # all_the_tweets = []
        # for i in accounts:
        #     new_tweets = self.api.user_timeline(screen_name=i, count=count)
        #     all_the_tweets.extend(new_tweets)
        #
        # for tweet in all_the_tweets:
        #     # Apply text_classifier here, return [1] label only
        #     if classifier(tweet.text) == 1:
        #         print(tweet.text)
        #     else:
        #         pass

        # return [for text in all_the_tweets].text

    def scrape(self, terms=None, accounts=None, count=None, geocode=None):
        # type: (Scraper, Set[str], Set[str], int, str) -> Dict[str, List[Status]]
        """
        General-purpose scraping method. Can scrape search terms, and accounts.

        :param geocode: Geographical area to search in. Can be blank.
        :param terms:  List of terms to search for.
        :param accounts: List of account names to search.
        :param count: Maximum tweets to return per search term.
        :return: A dictionary containing {'search-term': List[Status]} pairs.

        Examples:
            >>> scrape(geocode="41.8297855,-87.666775,50mi", terms={"pizza", "waffles"}, maximum=3)
            {'pizza': {Status, Status, Status},
            'waffles': {Status, Status}}
        """
        if not count:
            count = self.default_count

        if (not terms) and (not accounts):
            raise ValueError("No terms or accounts specified.")

        return {
            "hi": {"cool_tweet", "cooler_tweet"}
        }