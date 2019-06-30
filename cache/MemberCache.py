#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append("..")
from DbHelper import *

class MemberCache:
    def __init__(self):
        self.id_cache = {}
        self.name_cache = {}
        self.db = DbHelper()
        self.get_cache()

    def get_cache(self):
        result = self.db.select("SELECT id, name, is_followed, is_traced FROM member")
        for item in result:
            self.id_cache[item[0]] = [item[1], item[2], item[3]]
            self.name_cache[item[1]] = item[0]

    def id_exist(self, id):
        return id in self.id_cache

    def name_exist(self, name):
        return name in self.name_cache

    def is_follow_by_id(self, id):
        return id in self.id_cache and self.id_cache[id][1]

    def update_download_by_id(self, id, state = True):
        self.id_cache[id][1] = state

    def add(self, id, name, is_followed = False, is_traced = False):
        self.id_cache[id] = [name, is_followed, is_traced]
        self.name_cache[name] = id


