#!/usr/bin/python3
# Coding:utf-8

# Author: jias
#   Date: 2016.01.11

"""
All database record need a primary key.
In our system, the primary key is 32bit string
UUID is a good choice for use.

Here is the usage:

uuid_instance = PrimaryIDGenerator.uuid_generator()

"""

import datetime
import uuid
import redis
import shortuuid
from com.nnit.solution.local import Constant


class PrimaryIDGenerator(object):

    @staticmethod
    def primary_id_generator():
        """
        数据库表的主键生成器
        """
        return str(shortuuid.uuid(Constant.UUID_SEED))


class RedisConnection(object):

    @staticmethod
    def get_redis_connection(host='localhost', port=6379, dbName=0):
        return redis.Redis(host=host, port=port, db=dbName)


class SessionGenerator(object):

    @staticmethod
    def session_generate():
        return uuid.uuid1(uuid.getnode(), datetime.datetime.now().microsecond)


class SortedValueGenerator(object):

    """
    返回一个long型的整数
    计算方法：
        1. 获取当前时间的毫秒数
        2. 当前时间的毫秒数再增加1000
    """
    @staticmethod
    def generate_releaseDateValue():
        return datetime.datetime.now().microsecond + 1000

    """
    返回一个折扣的值。这个值用于放在sorted set中排序
    计算方法：
        1. 获得当前的折扣数
        2. 根据不同的折扣类型，换算成同一个的一个值
           例如：1. 5折， 变成 5000 （所有折扣，根据折扣值，再乘以1000）
                2. 满一百减20， 变成 200 （满多少减多少， 根据减的数值，乘以10）
    当前，先支持第一种方式。其他中方式等日后有时间再继续

    :param discount_value  : 折扣数量
    :param discount_type   : 折扣类型
    """
    @staticmethod
    def generate_discount_value(discount_original_value, discount_type):
        pass
