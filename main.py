#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import threading
from twitch import check_twitch_start


if os.environ["IS_TWITCH"]:
    thread_twitch = threading.Thread(target=check_twitch_start)
    thread_twitch.start()
