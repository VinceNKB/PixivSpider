#!/usr/bin/env python3
# coding=utf-8

import sys
sys.path.append("..")
from DbHelper import *
from pixivpy3 import *
from download import *
import time

class DownHelper:
    def __init__(self):
        self.api = AppPixivAPI()

    def down_single_image(self, image):
        if not os.path.exists(image.directory_path):
            os.makedirs(image.directory_path)

        self.api.download(image.image_url, path=image.directory_path, name=image.image_name)
        image.is_download = True

    def down_image_set(self, image_set, sleep_time = 0):
        try:
            if not os.path.exists(image_set.illust_path):
                os.makedirs(image_set.illust_path)

            for image in image_set.image_list:
                self.api.download(image.image_url, path=image.directory_path, name=image.image_name, replace=False)
                image.is_download = True

                if sleep_time > 0:
                    time.sleep(sleep_time)
            return True
        except:
            return False

if __name__ == "__main__":
    db_helper = DbHelper()
    image_sets = db_helper.get_download_image_sets(condition = 'need_download = 1 and is_download = 0 and type != "ugoira"')

    down_helper = DownHelper()
    down_helper.down_image_set(image_sets[0])
