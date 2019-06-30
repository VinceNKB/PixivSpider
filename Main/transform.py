#!/usr/bin/env python3
# coding=utf-8
import re
"""
25057 https://i.pximg.net/img-master/img/2018/04/18/05/49/48/68284634_p0_master1200.jpg
=>
UPDATE member SET is_traced = 1, last_trace_time = "2018-04-18 00:00:00" where id = 25057;
"""

pattern = r"img/(\d{4}/\d{2}/\d{2})/"

data_list = []
with open("user_transform.txt", "r", encoding="utf-8") as read_file:
    for line in read_file:
        line = line.strip()
        if len(line) > 0:
            items = line.split()
            id = items[0]

            if len(items) == 1:
                data_list.append((id, None))
            else:
                searchObj = re.search(pattern, items[1])
                if searchObj:
                    date = searchObj.group(1)
                    data_list.append((id, date.replace("/", "-") + " 00:00:00"))

                else:
                    print("error : %s" % line)

with open("user_transform_result.txt", "w", encoding="utf-8") as write_file:
    for data in data_list:
        if data[1]:
            write_file.write("UPDATE member SET is_traced = 1, last_trace_time = \"%s\" where id = %s;\n" % (data[1], data[0]))
        else:
            write_file.write("UPDATE member SET is_traced = 1 where id = %s;\n" % (data[0]))

