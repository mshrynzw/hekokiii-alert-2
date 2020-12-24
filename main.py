#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import threading
from twitch import check_twitch_start


if __name__ == "__main__":
    if os.environ["IS_TWITCH"]:
        logging.debug("test")
        thread_twitch = threading.Thread(target=check_twitch_start)
        thread_twitch.start()
