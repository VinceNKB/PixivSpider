#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append("..")
from DbHelper import *

class IllustCache:
    def __init__(self):
        self.id_cache = {}
        self.db = DbHelper()
        self.get_cache()

    def get_cache(self):
        result = self.db.select("SELECT id, need_download, is_download, book, trace FROM illust")
        for item in result:
            self.id_cache[item[0]] = {'need_download': item[1] == 1, 'is_download': item[2] == 1, 'book': item[3] == 1, 'trace': item[4] == 1}

    def id_exist(self, id):
        return id in self.id_cache

    def add(self, id, need_download = True, is_download = False, book = False, trace = False):
        self.id_cache[id] = {'need_download': need_download, 'is_download': is_download, 'book': book, 'trace': trace}

    def illust_state(self, id):
        return self.id_cache[id]

if __name__ == "__main__":
    ic = IllustCache()
    ic.get_cache()
    print(ic.id_cache)
