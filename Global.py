#!/usr/bin/env python3
# coding=utf-8

import os

# PATH
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# CONFIG_PATH = os.path.join(BASE_PATH, "config.ini")
ACCOUNT_PATH = os.path.join(BASE_PATH, "account.ini")
# DATA_PATH = os.path.join(BASE_PATH, "data")
DATA_PATH = os.path.join(os.path.dirname(BASE_PATH), "data")
DATABASE_PATH = os.path.join(DATA_PATH, "db/pixivDB.db")
ILLUST_PATH = os.path.join(DATA_PATH, "illust")

# NAME
DATABASE_NAME = "pixivDB"

