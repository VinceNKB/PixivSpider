#!/usr/bin/env python3
# coding=utf-8

from Global import *
from DbHelper import *
import os

invalid_size = {0, 58}

def invalid_file_check(img_set_list, check_size = False):
    """
    :param img_set_list:
    :param check_size: False:only check existing
    :return: list of invalid
    """
    invalid_file_set = []

    for img_set in img_set_list:
        is_invalid = False
        img_list = img_set.image_list
        for img in img_list:
            img_path = os.path.join(img.directory_path, img.image_name)
            if not os.path.exists(img_path):
                is_invalid = True
                break

            if check_size and os.path.getsize(img_path) in invalid_size:
                is_invalid = True
                break

        if is_invalid:
            invalid_file_set.append(img_set)

    return invalid_file_set

def reset_download_state(invalid_img_sets):
    db_helper = DbHelper()
    update_list = []

    for img_set in invalid_img_sets:
        update_list.append([{"is_download": False}, {"id": img_set.illust_id}])

    db_helper.update("illust", update_list)

def remove_invalid_folder(invalid_img_sets):
    for it in invalid_img_sets:
        del_file(it.illust_path)

def  del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path,i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)
            os.rmdir(path_file)


if __name__ == "__main__":
    db_helper = DbHelper()
    img_set_list = db_helper.get_download_image_sets(condition='is_download = 1')
    invalid_img_sets = invalid_file_check(img_set_list, True)

    print("Invalid img_set num: %d" % len(invalid_img_sets))
    print("Illusion path:")
    for img_set in invalid_img_sets:
        print(img_set.illust_path)

    reset_download_state(invalid_img_sets)
    remove_invalid_folder(invalid_img_sets)

