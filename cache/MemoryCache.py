#!/usr/bin/env python3
# coding=utf-8
from .MemberCache import *
from .TagCache import *

class MemoryCache:
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(MemoryCache, "_instance"):
            with MemoryCache._instance_lock:
                if not hasattr(MemoryCache, "_instance"):
                    MemoryCache._instance = object.__new__(cls)
                    MemoryCache._instance.init()
        return MemoryCache._instance

    def init(self):
        self.MemberCache = MemberCache()
        self.TagCache = TagCache()

