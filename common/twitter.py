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


def get_trend(twitter):
    params = {'id': '23424856'}
    res = twitter.get("https://api.twitter.com/1.1/trends/place.json", params=params)

    names = []
    if res.status_code == 200:
        result = res.json()
        trends = result[0]['trends']
        for trend in trends:
            name = trend['name']
            if name.startswith('#'):
                names.append(name)
            else:
                names.append('#' + name)
    else:
        logging.error("Could not get trends. (STATUS_CODE: {0})".format(str(res.status_code)))

    return names


def send_tweet(str_tweet):
    twitter = OAuth1Session(CK, CS, AT, ATS)
    hash_tags = get_trend(twitter)

    for hash_tag in hash_tags:
        if len(str_tweet) + len(hash_tag) + 1 < 230:
            str_tweet += " "
            str_tweet += hash_tag
        else:
            break

    params = {'status': str_tweet}
    res = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params=params)

    if res.status_code == 200:
        logging.info("Sent Tweet.\n" + str_tweet)
    else:
        logging.error("Could not send Tweet. (STATUS_CODE: {0})\n".format(str(res.status_code)) + str_tweet)
