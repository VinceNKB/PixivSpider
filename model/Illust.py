#!/usr/bin/env python3
# coding=utf-8

import datetime

class Illust:
    def __init__(self, id, user_id, title, type, page_count, create_time, url_template, sanity_level = None, caption = None, need_download = True, is_download = False, download_time = None, favor = 0, image_path = None, trace = False, book = False):
        self.id = str(id)
        self.user_id = str(user_id)
        self.title = title
        self.sanity_level = sanity_level
        self.type = type
        self.page_count = page_count
        self.caption = caption
        self.create_time = create_time
        self.need_download = need_download
        self.is_download = is_download
        self.download_time = download_time
        self.favor = favor
        self.url_template = url_template
        self.add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.image_path = image_path
        self.trace = trace
        self.book = book


    def get_model(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'sanity_level': self.sanity_level,
            'type': self.type,
            'page_count': self.page_count,
            'caption': self.caption,
            'create_time': self.create_time,
            'book': self.book,
            'trace': self.trace,
            'need_download': self.need_download,
            'is_download': self.is_download,
            'download_time': self.download_time,
            'favor': self.favor,
            'url_template': self.url_template,
            'add_time': self.add_time,
            'image_path': self.image_path
        }

