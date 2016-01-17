#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
消息服务都定义在这个Service中
"""


class MessageService(object):

    def __init__(self):
        pass

    """
    提取当前热门的群发消息
    quantity_per_page：每页显示的数量, 默认为10条
     current_page_num：当前显示第几页，默认为第一页

    返回一个消息对象列表
    """
    def fetch_hot_msgs(self, quantity_per_page=10, current_page_num=1):
        pass