import tweepy
import webbrowser
import time
import re
from collections import Counter
# import twitter_credentials as credenitals
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

callback_uri = 'oob'
auth = tweepy.OAuthHandler(
    os.environ['API_KEY'], os.environ['API_SECRETE_KEY'], callback_uri)
auth.set_access_token(os.environ['ACCESS_TOKEN'],
                      os.environ['ACCESS_TOKEN_SECRET'])


api = tweepy.API(auth)
home_timeline = api.home_timeline()


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit=3600, stream_limit=60):
        self.stream_limit = (datetime.datetime.utcnow() +
                             datetime.timedelta(seconds=stream_limit))
        self.limit = (datetime.datetime.utcnow() -
                      datetime.timedelta(seconds=time_limit))
        self.happy_hastag_list = []
        super(MyStreamListener, self).__init__()

#     def on_data(self, status):
#         if (status.created_at) > self.limit:
#             for i in status.entities['hashtags']:
#                 print(i['text'])
#                 self.happy_hastag_list.append(i['text'])
#             return True
#         else:
#             return False

    def on_status(self, status):
        if (status.created_at > self.limit) and (datetime.datetime.utcnow() <= self.stream_limit):
            for i in status.entities['hashtags']:
                print(i['text'])
                self.happy_hastag_list.append(i['text'])
            return True
        else:
            return False

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False


def find_happiest_hashtag_from_list(hashtag_list):
    Counter(hashtag_list)
    hashtag_dict = Counter(hashtag_list)
    hashtag_dict = dict(hashtag_dict)
    happiest_hashtag = max(hashtag_dict, key=lambda k: hashtag_dict[k])
    print(happiest_hashtag)
    return happiest_hashtag
