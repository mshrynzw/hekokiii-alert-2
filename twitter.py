#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
from requests_oauthlib import OAuth1Session

CK = os.environ["CONSUMER_KEY"]
CS = os.environ["CONSUMER_SECRET"]
AT = os.environ["ACCESS_TOKEN"]
ATS = os.environ["ACCESS_TOKEN_SECRET"]

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')


def send_tweet(str_tweet):
    twitter = OAuth1Session(CK, CS, AT, ATS)
    params = {"status": str_tweet}
    res = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params=params)

    if res.status_code == 200:
        logging.info("Sent Tweet.\n" + str_tweet)
    else:
        logging.error("Could not send Tweet. (STATUS_CODE: {})\n".format(str(res.status_code)) + str_tweet)
