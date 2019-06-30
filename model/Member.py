#!/usr/bin/env python3
# coding=utf-8

class Member:
    def __init__(self, id, account, name, is_followed = False, is_traced = False, last_trace_time = None, favor = 0):
        self.id = str(id)
        self.account = account
        self.name = name
        self.is_followed = is_followed
        self.is_traced = is_traced
        self.last_trace_time = last_trace_time
        self.favor = favor # 0:normal  1:i mark his illust 2: his illust is good 3: i love it 4: real special

    def get_model(self):
       return {
           'id': self.id,
           'account': self.account,
           'name': self.name,
           'is_followed': self.is_followed,
           'is_traced': self.is_traced,
           'last_trace_time': self.last_trace_time,
           'favor': self.favor
       }
