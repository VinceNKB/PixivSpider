#!/usr/bin/env python3
# coding=utf-8

from Global import *
from DbHelper import *
import os


def get_user_id():
    pass

def get_undownload_illust():
    undownload_illust_set = set()
    illust_count = 0

    if os.path.exists(ILLUST_PATH):
        for user_id in os.listdir(ILLUST_PATH):
            user_illust_path = os.path.join(ILLUST_PATH, user_id)
            if os.path.isdir(user_illust_path):
                for illust_id in os.listdir(user_illust_path):
                    illust_path = os.path.join(user_illust_path, illust_id)
                    count = len(os.listdir(illust_path))
                    illust_count += count
                    if count == 0:
                        undownload_illust_set.add(illust_id)

    return undownload_illust_set, illust_count


def reset_download_state(illust_set):
    db_helper = DbHelper()
    update_list = []

    for illust_id in illust_set:
        update_list.append([{"is_download": False}, {"id": illust_id}])

    db_helper.update("illust", update_list)


if __name__ == "__main__":
    undownload_illust_set, count = get_undownload_illust()

    print(undownload_illust_set)
    print(len(undownload_illust_set))
    print(count)

    with open('undownload_illust.txt', 'w', encoding='utf-8') as writeFile:
        for x in undownload_illust_set:
            writeFile.write('%s\n' % x)

    reset_download_state(undownload_illust_set)




