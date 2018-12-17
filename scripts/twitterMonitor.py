#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import sys

if len(sys.argv) != 2:
    print("[!]twitterMonitor.py username")
    exit(-1)

try:
    import tweepy
except ImportError:
    raise Exception("[!]Tweepy not found")

"""Authentication process and API creation"""
def createAPI():
    load_dotenv()
    auth=tweepy.OAuthHandler(os.environ["API_KEY"],os.environ["API_KEY_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"],os.environ["ACCESS_TOKEN_SECRET"])
    return tweepy.API(auth)

class customListener(tweepy.StreamListener):

    def on_status(self,status):
        print(status.text)

twitterAPI = createAPI()
listener = customListener()
userID = twitterAPI.get_user(sys.argv[1]).id
stream = tweepy.Stream(auth=twitterAPI.auth,listener=customListener())
print(userID)
stream.filter(follow=[str(userID)])
