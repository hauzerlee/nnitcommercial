#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
商家的服务都定义在这个Service中
"""
import sys
from com.nnit.solution.local import Constant


class ShopService(object):

    def __init__(self):
        pass

    """
    返回热门的商店
    quantity_per_page: 每页显示几个商铺，默认是10个
    current_page_num： 当前第几页，默认是第一页
    """
    def hot_shops(self, quantity_per_page=10, current_page_num=1):
        pass

    """
    根据商店的评分，返回商店列表
    direction表示根据评分正序还是反序排列
    默认是返回
    """
    def shops_by_score(self, direction=Constant.SEARCHING_DIRECTION_DESC):
        pass

    """
    返回某个类型的商店列表
    """
    def shops_with_type(self, shop_type):
        pass

    """
    返回热门的团购列表
    quantity_per_page: 每页显示几个团购，默认是10个
    current_page_num:  当前第几页，默认是第一页
    """
    def hot_groupons(self, quantity_per_page=10, current_page_num=1):
        pass