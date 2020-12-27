#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata


def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1

    return count


def delete_east_asian_width_count(text, delete_count):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            text = text[:-2]
            count += 2
        else:
            text = text[:-1]
            count += 1
        if count > delete_count:
            break

    return text
