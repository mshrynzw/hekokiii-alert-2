#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from common.twitter import send_tweet

# 5chのURL
url = os.environ["5CH_URL"]
url_scrap = os.environ["5CH_URL_SCRAP"]
# ツイート判定用の文字数境界値
str_count_boundary_value = int(os.environ["TWEET_BBS_STR_COUNT_BOUNDARY_VALUE"])
# ツイート判定用のコメント番号の倍数
count_multiple = int(os.environ["TWEET_BBS_COUNT_MULTIPLE"])
# ツイートのテンプレート
str_tpl = os.environ["TWEET_TPL_BBS"]

# ログのフォーマットを定義
logging.basicConfig(level=logging.INFO, format='%(levelname)s : %(asctime)s : %(message)s')


# 掲示板を確認する
def check_bbs_count():
    try:
        # 【前処理】
        # オプション設定用
        options = Options()
        # GUI起動OFF（=True）
        options.headless = True
        # Chromeドライバを設定
        driver = webdriver.Chrome(chrome_options=options)

        driver.get(url_scrap)
        sleep(40)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_css_selector("a.d-continu").click()

        el_cnt_s = driver.find_elements_by_css_selector("div.r-head div strong")
        el_name_s = driver.find_elements_by_css_selector("span.clname")
        el_cmt_s = driver.find_elements_by_css_selector("div.clmess")

        el_cnt_list = []
        el_name_list = []
        el_cmt_list = []

        for elCnt in el_cnt_s:
            el_cnt_list.append(elCnt.text)
        for elName in el_name_s:
            el_name_list.append(elName.text)
        for elCmt in el_cmt_s:
            el_cmt_list.append(elCmt.text.lstrip())

        # 【後処理】
        driver.close()
        driver.quit()

    except Exception as e:
        logging.error(e)
        raise

    return el_cnt_list, el_name_list, el_cmt_list


def update_count(cnt_list):
    max_cnt_org = os.environ["5CH_COUNT"]

    max_cnt = 0
    for cnt in cnt_list:
        if max_cnt < int(cnt):
            max_cnt = int(cnt)

    os.environ["5CH_COUNT"] = str(max_cnt)

    return max_cnt_org


def send_tweet_bbs(cnt_list, nm_list, cmt_list, cnt_max_rog):
    try:
        i = 0
        for cnt in cnt_list:
            if int(cnt) > int(cnt_max_rog):

                # Tweet
                if not "http" in cmt_list[i] and (
                        len(cmt_list[i]) > str_count_boundary_value or int(cnt) % count_multiple == 0):
                    str_tweet = str_tpl.format(cnt, nm_list[i], cmt_list[i], url)
                    if len(str_tweet) > 140:
                        cnt_del_str = len(str_tweet) - 140
                        str_tweet = str_tpl.format(cnt, nm_list[i], cmt_list[i][:-cnt_del_str], url)
                    send_tweet(str_tweet)
            i += 1

    except Exception as e:
        logging.error(e)
        raise


def check_bbs():
    while True:
        try:
            count_list, name_list, comment_list = check_bbs_count()
            count_max_org = update_count(count_list)
            send_tweet_bbs(count_list, name_list, comment_list, count_max_org)

        except Exception as e:
            logging.error(e)
            pass

        finally:
            sleep(300)
