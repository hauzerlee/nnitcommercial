#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.18

"""
和商户相关的操作，都定义在这个dao中
"""

import sys
import redis
from com.nnit.solution.local import Constant
from com.nnit.solution.local.util import utils


class ShopRedisDAO(object):

    def __init__(self):
        # get the redis connection
        self.redis = utils.RedisConnection.get_redis_connection('localhost',6379,0)

    # -----------------------------------------------------------------------
    # 商户发布信息的方法
    # -----------------------------------------------------------------------

    """
    商户发布团购信息

    param: shop_id     商铺的id
    param: groupon_ids 需要发布的团购id列表（一个list）
    """
    def publish_groupons(self,shop_id, groupon_ids):
        # 依次加入到zset里，并根据serialNum自动排序
        for groupon_id in groupon_ids:
            serialNum = utils.SortedValueGenerator.generate_releaseDateValue() + shop_id * 10
            self.redis.zadd(Constant.HOT_GROUPONS, groupon_id, serialNum)

    """
    商户发布折扣信息

    param: shop_id      商铺的id
    param: discount_ids 需要发布的折扣id列表（一个list）
    """
    def publis_discounts(self, shop_id, discount_ids):
        # 依次加入到zset里，并根据serialNum自动排序
        for discount_id in discount_ids:
            redis.hget(Constant.DISCOUNT, discount_id) # 貌似还没有这个redis结构
            discount_value = utils.SortedValueGenerator.generate_discount_value()
            redis.zadd(Constant.DISCOUNTS_SORT, discount_id, discount_value)

    # -----------------------------------------------------------------------
    # 用户提取折扣、优惠券信息
    # -----------------------------------------------------------------------

    """
    用户从移动终端提取目前热门的折扣信息
    """
    def get_available_discounts(self):
        self.redis.smembers(Constant.DISCOUNTS_SORT)

    """
    用户从移动终端提取目前热门的团购信息
    """
    def get_available_groupons(self):
        self.redis.smembers(Constant.HOT_GROUPONS)