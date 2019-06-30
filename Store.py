#!/usr/bin/env python3
# coding=utf-8

import sqlite3
import threading
from Global import *
from cache.MemberCache import *
from cache.IllustCache import *
from cache.TagCache import *
from DbHelper import *
from model.Illust import *
from model.Member import *
from model.Tag import *
from model.Tagillust import *

class Store:
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Store, "_instance"):
            with Store._instance_lock:
                if not hasattr(Store, "_instance"):
                    Store._instance = object.__new__(cls)
                    Store._instance.init()
        return Store._instance

    def init(self):
        self.memberCache = MemberCache()
        self.tagCache = TagCache()
        self.illustCache = IllustCache()
        self.db = DbHelper()

    def handle_members(self, members):
        store_map = {}

        for member in members:
            if self.memberCache.id_exist(member.id):
                # print('catch memberCache')
                continue
            else:
                store_map[member.id] = member

        if len(store_map) == 0:
            return True
        elif self.db.insert('member', [m.get_model() for m in store_map.values()]):
            for v in store_map.values():
                self.memberCache.add(v.id, v.name)
            return True
        else:
            return False

    def handle_members_follow(self, members):
        member_add_map = {}
        member_update_map = {}

        for member in members:
            if self.memberCache.is_follow_by_id(member.id):
                # print('catch memberCache')
                continue
            elif self.memberCache.id_exist(member.id):
                member_update_map[member.id] = member
            else:
                member_add_map[member.id] = member

        if len(member_update_map) > 0:
            data_list = []
            for m in member_update_map:
                data_list.append([{"is_followed": True}, {"id": m}])
            if not self.db.update("member", data_list):
                return False

            for m in member_update_map:
                self.memberCache.update_download_by_id(m)

        if len(member_add_map) > 0:
            if self.db.insert('member', [m.get_model() for m in member_add_map.values()]):
                for v in member_add_map.values():
                    self.memberCache.add(v.id, v.name, v.is_followed, v.is_traced)
                return True
            else:
                return False

        return True

    def handle_illusts_book(self, illusts, need_download = True, is_download = False, book = True, trace = False):
        store_map = {}
        update_set = set()

        for illust in illusts:
            if self.illustCache.id_exist(illust.id):
                if not self.illustCache.illust_state(illust.id)['book']:
                    update_set.add(illust.id)
            else:
                store_map[illust.id] = illust

        # print([x for x in update_set])

        if len(update_set) > 0:
            data_list = []
            for key in update_set:
                data_list.append([{'book': True}, {'id': key}])
            if self.db.update('illust', data_list):
                for key in update_set:
                    self.illustCache.id_cache[key]['book'] = True
            else:
                return False

        if len(store_map) == 0:
            return True
        elif self.db.insert('illust', [m.get_model() for m in store_map.values()]):
            for v in store_map.values():
                self.illustCache.add(v.id, need_download, is_download, book, trace)
            return True
        else:
            return False

    def handle_illusts_trace(self, illusts, need_download = True, is_download = False, book = False, trace = True):
        store_map = {}
        update_set = set()

        for illust in illusts:
            if self.illustCache.id_exist(illust.id):
                if not self.illustCache.illust_state(illust.id)['trace']:
                    update_set.add(illust.id)
            else:
                store_map[illust.id] = illust

        if len(update_set) > 0:
            data_list = []
            for key in update_set:
                data_list.append([{'trace': True}, {'id': key}])
            if self.db.update('illust', data_list):
                for key in update_set:
                    self.illustCache.id_cache[key]['trace'] = True
            else:
                print("exp wee")
                return False

        if len(store_map) == 0:
            return True
        elif self.db.insert('illust', [m.get_model() for m in store_map.values()]):
            for v in store_map.values():
                self.illustCache.add(v.id, need_download, is_download, book, trace)
            return True
        else:
            print("exp sd")
            return False


    def handle_tags(self, tags):
        store_map = {}

        for tag in tags:
            if self.tagCache.name_exist(tag.name):
                continue
            else:
                store_map[tag.name] = tag

        if len(store_map) == 0:
            return True
        elif self.db.insert('tag', [m.get_model() for m in store_map.values()]):
            for v in store_map.values():
                tag_id = self.db.tag_check(v.name)
                self.tagCache.add(tag_id, v.name)
            return True
        else:
            return False

    def handle_tagIllusts(self, tag_map):
        tagillust_list = []

        for illust_id, tag_set in tag_map.items():
            for tag_name in tag_set:
                if self.tagCache.name_exist(tag_name):
                    tag_id = self.tagCache.get_id(tag_name)
                    tagillust_list.append(Tagillust(illust_id, tag_id))

        self.db.insert("tagillust", [ti.get_model() for ti in tagillust_list])

    def update_trace_time(self, user_id):
        self.db.update("member", [[{"last_trace_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {"id": user_id}]])

    def get_member_set(self, condition = "is_traced = 1"):
        return self.db.get_member_set(condition = condition)

