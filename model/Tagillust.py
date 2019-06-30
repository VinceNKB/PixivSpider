#!/usr/bin/env python3
# coding=utf-8

class Tagillust:
    def __init__(self, illust_id, tag_id):
        self.illust_id = illust_id
        self.tag_id = tag_id

    def get_model(self):
        return {
            'illust_id': self.illust_id,
            'tag_id': self.tag_id
        }