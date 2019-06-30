#!/usr/bin/env python3
#coding=utf8

import json
import datetime
from pixivpy3 import *
#from downloader import IMGDownloader
import time
import configparser
from Global import *
from Store import *
from model.Illust import *
from model.Member import *
from model.Tag import *
from model.Tagillust import *
import urllib.parse

class PixivParser:
    def __init__(self):
        self.api = AppPixivAPI()
        self.error = []
        self.store = Store()


    def load_account_config(self):
        accountConfig = configparser.ConfigParser()
        accountConfig.read(ACCOUNT_PATH)
        self.username = accountConfig['pixiv']['user']
        self.password = accountConfig['pixiv']['password']
        self.userid = accountConfig['pixiv']['userid']
        # print(self.username, self.password)
        return accountConfig['pixiv']['user'], accountConfig['pixiv']['password']

    def login_with_default_account(self):
        self.api.login(self.username, self.password)

    def login(self, usrname, password):
        self.api.login(usrname, password)

    def start_trace(self):
        member_set = self.store.get_member_set(condition = "is_traced = 1")
        total_num = len(member_set)
        cur_num = 0
        for member in member_set:
            cur_num += 1
            # print("start trace user_id " + member.id)
            last_trace_time = self.str_to_timestramp(member.last_trace_time) if member.last_trace_time else 0
            if int(time.time()) - last_trace_time <= 24 * 60 * 60:
                continue

            print("Progress: %d / %d" % (cur_num, total_num))

            if not self.trace(member, last_trace_time, type = "illust"):
                print("download trace illust fail because of insert illusts error. Member info")
                print(member.id + " " + member.name+" illust "+ (member.last_trace_time if member.last_trace_time else "0"))
                print("-------------------------------------------------------------------")
                continue
            if not self.trace(member, last_trace_time, type = "manga"):
                print("download trace illust fail because of insert illusts error. Member info")
                print(member.id + " " + member.name+" manga "+ (member.last_trace_time if member.last_trace_time else "0"))
                print("-------------------------------------------------------------------")
                continue

            # to update the member last trace time in the end
            self.store.update_trace_time(member.id)

    def trace(self, member, last_trace_time, type = "illust"):
        print("in trace " + member.id + " " + str(last_trace_time) + " " +type)
        try:
            cur_offset = None
            while cur_offset != "END":
                # print("cur_offset " + "0" if not cur_offset else str(cur_offset))
                time.sleep(1)
                print("begin")
                result = self.api.user_illusts(int(member.id), type = type, offset = cur_offset) # 有时会出现相当长段时间的停顿，无法理解
                print("end")
                if result.next_url is None:
                    cur_offset = "END"
                else:
                    cur_offset = int(urllib.parse.parse_qs(urllib.parse.urlparse(result.next_url).query)['offset'][0])

                illust_set = self.parse_trace_result(result, last_trace_time)

                if len(illust_set) == 0:
                    cur_offset = "END"
                elif not self.store.handle_illusts_trace(illust_set):
                    print("exp iuihi")
                    return False
            return True
        except Exception as e:
            print("exp ihisdsd")
            print(e)
            return False

    def parse_trace_result(self, result_json, last_trace_time):
        def parse_time(time_str): # 2018-09-09T08:52:10+09:00
            items = time_str.strip().split("T")
            return items[0] + " " + items[1].split("+")[0]

        illust_set = []

        for illust in result_json.illusts:
            # print("illust create time " + parse_time(illust.create_date))
            illust_create_timestrapmp = self.str_to_timestramp(parse_time(illust.create_date))

            if illust_create_timestrapmp <= last_trace_time:
                return illust_set

            if illust.page_count == 1:
                first_url = illust.meta_single_page.original_image_url.strip()
            else:
                first_url = illust.meta_pages[0].image_urls.original.strip()

            if "limit" in first_url:
                url_template = first_url
            elif illust.type == "ugoira":
                url_template = first_url.split("ugoira")[0] + "ugoira%d."+ first_url[-3:]
            else:
                url_template = first_url.split("_p")[0] + "_p%d."+ first_url[-3:]

            illust = Illust(illust.id, illust.user.id, illust.title, illust.type, illust.page_count, illust.create_date, url_template, illust.sanity_level, illust.caption, favor = 1, trace = True, book = False) # attention that the book attribute is probable to be true
            illust_set.append(illust)

        return illust_set

    def get_all_my_bookmark(self, page_count = sys.maxsize):
        self.get_my_bookmark(restrict='public', page_count = page_count)
        self.get_my_bookmark(restrict='private', page_count = page_count)


    def get_my_bookmark(self, restrict='public', page_count = sys.maxsize, start_id = None):
        count = 1
        max_bookmark_id = start_id
        while max_bookmark_id != 'END' and count <= page_count:
            bookmark_list = self.api.user_bookmarks_illust(self.userid, restrict=restrict, filter='for_ios', max_bookmark_id=max_bookmark_id, tag=None, req_auth=True)
            print(bookmark_list.next_url)
            max_bookmark_id = self.parse_max_bookmark_id(bookmark_list.next_url)
            member_list = []
            illust_list = []
            tag_map = {}
            tag_sets = set()

            for bm in bookmark_list.illusts:
                # bookmark_store.append(bm.id)
                member, illust, tag_set = self.parse_bookmark(bm)
                member_list.append(member)
                illust_list.append(illust)
                tag_sets = tag_sets | tag_set
                tag_map[illust.id] = tag_set

            tag_list = [Tag(t) for t in tag_sets]

            if not self.store.handle_members(member_list):
                # log
                print("download bookmark fail because of insert members error. Illust info")
                for illust in illust_list:
                    print(illust.id + " " + illust.title)
                print("-------------------------------------------------------------------")
                continue

            if not self.store.handle_illusts_book(illust_list):
                # log
                print("download bookmark fail because of insert illusts error. Illust info")
                for illust in illust_list:
                    print(illust.id + " " + illust.title)
                print("-------------------------------------------------------------------")
                continue

            if not self.store.handle_tags(tag_list):
                # log
                print("download bookmark fail because of insert tags error. Illust info")
                for illust in illust_list:
                    print(illust.id + " " + illust.title)
                print("-------------------------------------------------------------------")
                continue

            self.store.handle_tagIllusts(tag_map)

            print(max_bookmark_id, count)
            # bookmark_store.extend(public_bookmark_list.illusts)
            time.sleep(2)
            count += 1
        # with open('bookmark_private.json', 'w') as jsonFile:
        #     for bs in bookmark_store:
        #         jsonFile.write('%s\n' % bs)

    def parse_max_bookmark_id(self, next_url):
        if next_url == None:
            return 'END'
        for str in next_url.split('?')[1].split('&'):
            if str.startswith('max_bookmark_id'):
                return str.split('=')[1]
        return ''

    def parse_bookmark(self, bookmark_json):
        member = Member(bookmark_json.user.id, bookmark_json.user.account, bookmark_json.user.name,favor = 1)
        # print(bookmark_json)

        if bookmark_json.page_count == 1:
            first_url = bookmark_json.meta_single_page.original_image_url.strip()
        else:
            first_url = bookmark_json.meta_pages[0].image_urls.original.strip()

        if "limit" in first_url:
            url_template = first_url
        elif bookmark_json.type == "ugoira":
            url_template = first_url.split("ugoira")[0] + "ugoira%d."+ first_url[-3:]
        else:
            url_template = first_url.split("_p")[0] + "_p%d."+ first_url[-3:]

        illust = Illust(bookmark_json.id, bookmark_json.user.id, bookmark_json.title, bookmark_json.type, bookmark_json.page_count, bookmark_json.create_date, url_template, bookmark_json.sanity_level, bookmark_json.caption, favor = 0, book = True)

        tag_set = set()
        for tag in bookmark_json.tags:
            tag_set.add(tag.name)

        return member, illust, tag_set

    def get_following_info(self):
        self.public_follow = []
        self.private_follow = []

        next_page = 1
        while next_page != None:
            followDict = self.papi.me_following(page=next_page, per_page=30, publicity='public')
            self.public_follow.extend(followDict.response)
            next_page = followDict.pagination.next

        next_page = 1
        while next_page != None:
            followDict = self.papi.me_following(page=next_page, per_page=30, publicity='private')
            self.private_follow.extend(followDict.response)
            next_page = followDict.pagination.next

        return self.public_follow, self.private_follow

    def save_following(self, base):
        with open(base + '/follow_public.json', 'w') as jsonFile:
            json.dump(self.public_follow, jsonFile)

        with open(base + '/follow_private.json', 'w') as jsonFile:
            json.dump(self.private_follow, jsonFile)

    def load_following(self, base):
        with open(base + '/follow_public.json', 'r') as jsonFile:
            self.public_follow = json.load(jsonFile)

        with open(base + '/follow_private.json', 'r') as jsonFile:
            self.private_follow = json.load(jsonFile)

    def get_all_image_info(self, usrId):
        next_page = 1
        image_list = []
        while next_page != None:
            image = self.papi.users_works(usrId, page=next_page, per_page=30)
            image_list.extend(image.response)
            next_page = image.pagination.next

        return image_list

    def get_usr_info(self, usr_dict):
        usr_info = {}
        usr_info['id'] = usr_dict['id']
        usr_info['account'] = usr_dict['account']
        usr_info['name'] = usr_dict['name']
        usr_info['profile_image_urls'] = usr_dict['profile_image_urls']
        usr_info['image_list'] = self.get_all_image_info(usr_info['id'])
        usr_info['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return usr_info

    def get_usrs_info(self):
        if not (self.public_follow or self.private_follow):
            self.get_following_info()
        usr_list = self.public_follow + self.private_follow
        self.usrs_info = []
        count = 0
        for usr_dict in usr_list:
            count += 1
            if count == 10:
                break
            print(usr_dict['account'])
            try:
                t_cur_usr = self.get_usr_info(usr_dict)
            except Exception:
                self.error.append(usr_dict)
                continue
            self.usrs_info.append(t_cur_usr)
            time.sleep(3)
        return self.usrs_info


    def save_usrs_info(self, base_path):
        with open(base_path + '/usr_info.json', 'w') as jsonFile:
            json.dump(self.usrs_info, jsonFile)

    def load_usrs_info(self, base_path):
        with open(base_path + '/usr_info.json', 'r') as jsonFile:
            self.usrs_info = json.load(jsonFile)

        return self.usrs_info

    def fetch_following(self, restrict="public", page_count = sys.maxsize, start_id = None):
        cur_offset = start_id
        count = 0
        while cur_offset != "END" and count < page_count:
            count += 1

            member_list = []
            result = self.api.user_following(self.userid, restrict=restrict, offset=cur_offset, req_auth=True)

            if result.next_url is None:
                cur_offset = "END"
            else:
                cur_offset = int(urllib.parse.parse_qs(urllib.parse.urlparse(result.next_url).query)['offset'][0])

            print("count: %d, cur_offset: %s" % (count, str(cur_offset)))

            for user_preview in result.user_previews:
                # print(user_preview.illusts)
                user = user_preview.user
                member = Member(user.id, user.account, user.name,is_followed = True, favor = 1)
                member_list.append(member)

            if not self.store.handle_members_follow(member_list):
                # log
                print("fetch following fail because of insert members error. Members info")
                for member in member_list:
                    print(member.id + " " + member.name)
                print("-------------------------------------------------------------------")

    def str_to_timestramp(self, time_str):
        return int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S")))

    def test(self):
        json_result = self.api.user_illusts(660788)


if __name__ == '__main__':
    pp = PixivParser()
    pp.load_account_config()
    pp.login_with_default_account()

    #pp.get_all_my_bookmark()
    #pp.get_my_bookmark(restrict='public', page_count=5, start_id=None)
    #pp.fetch_following(page_count=1)
    pp.start_trace()




