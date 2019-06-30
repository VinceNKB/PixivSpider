#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append("..")
from DbHelper import *
from download.DownHelper import *
import time

class log:
    def __init__(self):
        self.file_handle = open("log", "w", encoding="utf-8")

    def write(self, info):
        self.file_handle.write("%s\n" % info)
        
    def __del__(self):
        self.file_handle.close()


if __name__ == "__main__":
    db_helper = DbHelper()
    image_sets = db_helper.get_download_image_sets(condition = 'need_download = 1 and is_download = 0 and user_id != 0 and type != "ugoira"')
    print("total count of images : %d" % len(image_sets))
    down_helper = DownHelper()
    my_log = log()

    count = 0
    for image_set in image_sets:
        log_str = "No.%d download %s user %s at %s" % (count, image_set.illust_id, image_set.user_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(log_str)

        down_helper.down_image_set(image_set, 0.5)
        db_helper.update_download(image_set.illust_id, image_set.illust_path)
        count += 1

        my_log.write(log_str)