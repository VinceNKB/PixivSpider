#!/usr/bin/env python3
# coding=utf-8

class Tag:
    def __init__(self, name, count = 0, favor = 0):
        self.name = name
        self.count = count
        self.favor = favor

    def get_model(self):
        return {
            'name': self.name,
            'count': self.count,
            'favor': self.favor
        }
