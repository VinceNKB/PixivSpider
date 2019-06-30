#!/usr/bin/env python3
# coding=utf-8

import sqlite3
import threading
from Global import *
from model.Member import *
from download.ImageSet import *
import datetime

class DbHelper:
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(DbHelper, "_instance"):
            with DbHelper._instance_lock:
                if not hasattr(DbHelper, "_instance"):
                    DbHelper._instance = object.__new__(cls)
                    DbHelper._instance.__connect_database()
        return DbHelper._instance

    def __connect_database(self):
        self.db_path = DATABASE_PATH
        self.__connection = sqlite3.connect(self.db_path)
        self.__cursor = self.__connection.cursor()

    def insert(self, table, data_list):
        '''
        :param table: table name
        :param data_list: [{col1:val1, col2:val2, ...}, ...]
        :return:
        '''
        if not data_list or not len(data_list):
            return False

        sql_template = '''INSERT INTO %s(%s) VALUES (%s)'''

        try:
            for data in data_list:
                column = tuple(data.keys())
                sql = sql_template % (table, ', '.join(column), ', '.join(['?']*len(column)))

                task = [data[key] for key in column]
                # print(sql)
                # print(task)
                self.__cursor.execute(sql, task)
            self.__connection.commit()
            return True
        except:
            return False


    def update(self, table, data_list):
        '''
        :param table:
        :param data_list: [[{(update)col1:val1, col2:val2, ...},{(condition)col1:val1, col2:val2, ...}], ...]
        :return:
        '''
        if not data_list or not len(data_list):
            return False

        sql_template = '''UPDATE %s SET %s WHERE %s'''
        try:
            for data in data_list:
                update_column = tuple(data[0].keys())
                condition_column = tuple(data[1].keys())

                sql = sql_template % (table, ', '.join(['%s = ?' % col for col in update_column]), ' and '.join(['%s = ?' % col for col in condition_column]))
                task = ([data[0][key] for key in update_column] + [data[1][key] for key in condition_column])
                self.__cursor.execute(sql, task)
            self.__connection.commit()
            return True
        except:
            return False


    def insert_illust(self, illust_list):
        sql = '''INSERT INTO illust(id, userid, title, is_bookmarked, sanity_level, type, page_count, caption, create_time, add_time, need_download, is_download, download_time, favor, path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        try:
            for illust in illust_list:
                task = (illust['id'], illust['userid'], illust['title'], illust['is_bookmarked'], illust['sanity_level'], illust['type'], illust['page_count'], illust['caption'], illust['create_time'], illust['add_time'], illust['need_download'], illust['is_download'], illust['download_time'], illust['favor'], illust['path'])
                self.__cursor.execute(sql, task)
            self.__connection.commit()
            return True
        except:
            return False


    def userid_check(self, user_id):
        try:
            self.__cursor.execute("SELECT count(1) FROM member WHERE id=?", (user_id,))
            return self.__cursor.fetchone()[0] == 1
        except:
            return None


    def select(self, sql):
        try:
            self.__cursor.execute(sql)
            return self.__cursor.fetchall()
        except:
            return None


    # def illust_check(self, illust_id):
    #     cursor = self.__connection.cursor()
    #     try:
    #         cursor.execute("SELECT count(1) FROM illust WHERE id=?", (illust_id,))
    #         return cursor.fetchone()[0] == 1
    #     except:
    #         return None
    #     finally:
    #         cursor.close()

    def get_download_image_sets(self, condition = 'need_download = 1 and is_download = 0'):
        """
        :param condition: 'need_download = 1 and is_download = 0'
        :return:
        """
        if condition:
            sql = "SELECT id, page_count, user_id, url_template from illust where %s" % condition
        else:
            sql = "SELECT id, page_count, user_id, url_template"

        result = self.select(sql)
        image_set_list = []
        for item in result:
            image_set_list.append(ImageSet(item[0], item[1], item[2], item[3]))
        return image_set_list

    def get_member_set(self, condition = "is_traced = 1"):
        if condition:
            sql = "SELECT id, account, name, is_followed, is_traced, last_trace_time, favor from member where %s" % condition
        else:
            sql = "SELECT id, account, name, is_followed, is_traced, last_trace_time, favor from member"

        result = self.select(sql)
        member_set = []
        for item in result:
            member_set.append(Member(id = item[0], account = item[1], name = item[2], is_followed = item[3], is_traced = item[4], last_trace_time = item[5], favor = item[6]))

        return member_set

    def update_download(self, illust_id, download_path):
        #data_list: [[{(update)col1:val1, col2:val2, ...},{(condition)col1:val1, col2:val2, ...}], ...]
        data_list = [[{"is_download": True, "image_path": download_path, "download_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {"id": illust_id}]]
        self.update("illust", data_list)


    def tag_check(self, tagname):
        try:
            self.__cursor.execute("SELECT id FROM tag WHERE name=?", (tagname,))
            return self.__cursor.fetchone()[0]
        except:
            return None

    def close_db(self):
        if not self.__cursor:
            self.__cursor.close()
            self.__cursor = None
        if not self.__connection:
            self.__connection.close()
            self.__connection = None

    def __del__(self):
        if not self.__connection or not self.__cursor:
            self.close_db()


if __name__ == "__main__":
    db = DbHelper()
    # print(db.insert('member', [Member('1', '2', '3').get_model()]));
    print(db.select("SELECT id, page_count, user_id, create_time from illust where need_download = 1 and is_download = 0"))
