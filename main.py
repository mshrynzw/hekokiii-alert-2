#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import threading
from twitch import check_twitch_start

logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')


logging.debug("start main")
if os.environ["IS_TWITCH"]:
    logging.debug("enter true")
    thread_twitch = threading.Thread(target=check_twitch_start)
    thread_twitch.start()
