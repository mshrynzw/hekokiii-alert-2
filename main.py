#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import threading
from app.bbs import check_bbs
from app.twitter import check_twitter
from app.twitch import check_twitch_start


if __name__ == '__main__':
    if os.environ['IS_TWITCH']:
        thread_twitch = threading.Thread(target=check_twitch_start)
        thread_twitch.start()

    if os.environ['IS_TWITTER']:
        thread_twitter = threading.Thread(target=check_twitter)
        thread_twitter.start()

    if os.environ['IS_5CH']:
        thread_5ch = threading.Thread(target=check_bbs)
        thread_5ch.start()
