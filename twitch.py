#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import requests
from twitter import send_tweet

client_id = os.environ["TWITCH_CLIENT_ID"]
client_secret = os.environ["TWITCH_CLIENT_SECRET"]
search_query = os.environ["TWITCH_SEARCH_QUERY"]
TWEET_TPL = os.environ["TWEET_TPL_TWITCH_START"]

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')


def authenticate():
    params = {
        'client_id': 'value1',
        'client_secret': 'value2',
        'grant_type': 'client_credentials'
    }
    res = requests.get("https://id.twitch.tv/oauth2/token", params=params)

    if res.status_code == 200:
        result = res.json()
        access_token = result['access_token']
        logging.info("Got Twitch API access token.")
        return access_token
    else:
        logging.error("Could not authenticate Twitch API. (STATUS_CODE: {})".format(res.status_code))
        return None


def check_twitch_start():
    access_token = authenticate()

    while True:

        params = {
            'query': search_query
        }
        headers = {
            'Client-ID': client_id,
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Authorization': 'Bearer ' + str(access_token)
        }
        res = requests.get("https://api.twitch.tv/helix/search/channels", params=params, headers=headers)

        if res.status_code == 200:
            result = res.json()
            data = result['data']
            title = result['data']['title']
            if len(data) == 0:
                logging.info("There are not Twitch channel info.")
            else:
                send_tweet(TWEET_TPL)
        else:
            logging.error("Could not get Twitch channel info. (STATUS_CODE: {})".format(str(res.status_code)))
