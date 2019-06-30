#!/usr/bin/env python3
# coding=utf-8

from Global import *
import os

class ImageSet:
    def __init__(self, illust_id, image_num, user_id, url_template):
        self.illust_id = illust_id
        self.image_num = image_num
        self.user_id = user_id
        self.user_path = os.path.join(ILLUST_PATH, self.user_id)
        self.illust_path = os.path.join(self.user_path, self.illust_id)
        self.url_path_template = url_template
        self.image_name_template = "%d." + url_template[-3:]
        self.image_list = []
        self.fill_image_set()
        #https: //i.pximg.net/img-original/img/2014/12/14/01/49/55/47546994_p31.jpg

    def fill_image_set(self):
        for i in range(self.image_num):
            self.image_list.append(Image(self.image_name_template % i, self.url_path_template % i, self.illust_path))

class Image:
    def __init__(self, image_name, image_url, directory_path):
        self.image_name = image_name
        self.image_url = image_url
        self.directory_path = directory_path
        self.is_download = False




if __name__ == "__main__":
    path = "https://i.pximg.net/img-original/img/%s/%s_p%s.jpg" % ("2014", "2323232", "%s")
    print(path)
