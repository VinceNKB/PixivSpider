#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append("..")
from DbHelper import *
from download.DownHelper import *
import time

if __name__ == "__main__":
    db_helper = DbHelper()
    image_sets = db_helper.get_download_image_sets(condition = 'need_download = 1 and is_download = 0 and user_id != 0')
    down_helper = DownHelper()

    count = 0
    for image_set in image_sets:
        down_helper.down_image_set(image_set, 0.5)
        db_helper.update_download(image_set.illust_id, image_set.illust_path)

        count += 1
        print("No.%d download %s user %s at %s" % (count, image_set.illust_id, image_set.user_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))



