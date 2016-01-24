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
        self.redis = utils.RedisConnection.get_redis_connection()

    # -----------------------------------------------------------------------
    # 商户发布信息的方法
    # -----------------------------------------------------------------------

    """
    商户发布团购信息

    param: shop_id     商铺的id
    param: groupon_ids 需要发布的团购id列表（一个list）
    """
    def publish_groupons(self, shop_id, groupon_ids):
        # 依次加入到zset里，并根据serialNum自动排序
        for groupon_id in groupon_ids:
            serial_num = utils.SortedValueGenerator.generate_releaseDateValue() + shop_id * 10
            self.redis.zadd(Constant.HOT_GROUPONS, groupon_id, serial_num)

    """
    商户发布折扣信息
    (貌似管理平台需要传入很多参数。需要和Oliver协商)

    param: shop_id      商铺的id
    param: discount_ids 需要发布的折扣id列表（一个map）
                        key: production_id
                        value: discount_id
    param: discount_values 需要发布的折扣的值（一个map）
                        key: production_id
                        value: discount_value
    """
    def publis_discounts(self, shop_id, discount_ids_map, discount_values_map):
        # 依次加入到zset里，并根据serialNum自动排序
        for production_id in discount_ids_map:
            """ 创建一个折扣的redis对象 """
            """ key是 Discount:discountId """
            redis_key_discount = Constant.DISCOUNT + discount_ids_map[production_id]
            self.redis.hmset(redis_key_discount, production_id, discount_values_map[production_id])

            """ 放到公共的redis折扣列表里 """
            self.redis.hmset(Constant.DISCOUNTS_SORT,
                             discount_ids_map[production_id],
                             discount_values_map[production_id])

    # -----------------------------------------------------------------------
    # 用户提取折扣、优惠券信息
    # -----------------------------------------------------------------------

    """
    用户从移动终端提取目前热门的折扣信息
    """
    def get_available_discounts(self):
        return self.redis.smembers(Constant.DISCOUNTS_SORT)

    """
    用户从移动终端提取目前热门的团购信息
    """
    def get_available_groupons(self):
        return self.redis.smembers(Constant.HOT_GROUPONS)