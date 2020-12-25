#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import threading
from twitch import check_twitch_start
from bbs import check_bbs


if __name__ == "__main__":
    if os.environ["IS_TWITCH"]:
        thread_twitch = threading.Thread(target=check_twitch_start)
        thread_twitch.start()

    if os.environ["IS_5CH"]:
        thread_5ch = threading.Thread(target=check_bbs)
        thread_5ch.start()