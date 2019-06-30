#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append("..")
from DbHelper import *

class TagCache:
    def __init__(self):
        self.id_cache = {}
        self.name_cache = {}
        self.db = DbHelper()
        self.get_cache()

    def get_cache(self):
        result = self.db.select("SELECT id, name FROM tag")
        for item in result:
            self.id_cache[item[0]] = item[1]
            self.name_cache[item[1]] = item[0]

    def id_exist(self, id):
        return id in self.id_cache

    def name_exist(self, name):
        return name in self.name_cache

    def get_id(self, tag_name):
        return self.name_cache[tag_name]

    def add(self, id, name):
        self.id_cache[id] = name
        self.name_cache[name] = id


