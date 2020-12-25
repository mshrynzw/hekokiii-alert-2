#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
import logging
import os
from requests_oauthlib import OAuth1Session
from time import sleep
from common.twitter import send_tweet

# Twitter用の設定
CK = os.environ["CONSUMER_KEY"]
CS = os.environ["CONSUMER_SECRET"]
AT = os.environ["ACCESS_TOKEN"]
ATS = os.environ["ACCESS_TOKEN_SECRET"]
# Twitter検索の設定
keyword = os.environ["TWITTER_SEARCH_EXCLUSION"]
from_user_list = os.environ["TWITTER_SEARCH_FROM_USER"].split(',')

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')


def check_twitter():
    while True:
        # 5分前の日時
        since_datetime = (datetime.date.today() - datetime.timedelta(minutes=5)).strftime('%Y-%m-%d_%H:%M')
        since_datetime += ':00_JST'
        logging.info(since_datetime)

        for from_user in from_user_list:
            # ツイート検索
            url = "https://api.twitter.com/1.1/search/tweets.json"
            if keyword is None:
                query = "from:" + from_user + " since:" + since_datetime
            else:
                query = "-" + keyword + " from:" + from_user + " since:" + since_datetime
            params = {'q': query, 'count': 10}
            twitter = OAuth1Session(CK, CS, AT, ATS)
            res = twitter.get(url, params=params)

            if res.status_code == 200:  # 正常に検索できた場合
                results = json.loads(res.text)
                for status in results['statuses']:
                    # ツイート送信
                    str_tweet = status['text']
                    send_tweet(str_tweet)

        sleep(300)
