#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import json
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
# ツイートのテンプレート
str_tmp = os.environ["TWEET_TPL_TWITTER"]


def check_twitter():
    while True:
        # 本日の日付を取得
        today = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        for from_user in from_user_list:
            # ツイート検索
            url = "https://api.twitter.com/1.1/search/tweets.json"
            if keyword is None:
                query = "from:" + from_user + " since:" + today
            else:
                query = "-" + keyword + " from:" + from_user + " since:" + today
            params = {'q': query, 'count': 10}
            twitter = OAuth1Session(CK, CS, AT, ATS)
            res = twitter.get(url, params=params)

            if res.status_code == 200:  # 正常に検索できた場合
                results = json.loads(res.text)
                for tweet in results['statuses']:
                    # ツイート送信
                    str_tweet = str_tmp.format(text=tweet['text'])
                    send_tweet(str_tweet)
                    sleep(360)

        sleep(60)
