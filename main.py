#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import threading
from twitch import check_twitch_start


if __name__ == "__main__":
    if os.environ["IS_TWITCH"]:
        thread_twitch_00 = threading.Thread(target=check_twitch_start)
        thread_twitch_00.start()
