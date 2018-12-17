#!/usr/bin/env python3

try:
    import tweepy
except ImportError:
    raise Exception("[!]Tweepy not found")

"""Authentication process and API creation"""
def createAPI():

class customListener(tweepy.StreamListener):

    def on_status(self,status):
        print(status.text)

listener = customListener()
stream = tweepy.Stream(auth)
