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
        return str(shortuuid.uuid())


class RedisConnection(object):
    @staticmethod
    def get_redis_connection(host='localhost', port=6379, charset='GBK', dbName=0):
        return redis.Redis(host=host, port=port, db=dbName)


class SessionGenerator(object):
    @staticmethod
    def session_generate():
        return str(shortuuid.uuid())


class SortedValueGenerator(object):

    @staticmethod
    def generate_releaseDateValue():
        """
        计算方法：
          1. 获取当前时间的毫秒数
          2. 当前时间的毫秒数再增加1000

        :return 返回一个long型的整数
        """
        return datetime.datetime.now().microsecond + 1000

    @staticmethod
    def generate_discount_value(discount_original_value, discount_type):
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
        pass

def getDatetToLong():
    """
    #把日期转化成int（long），用户商铺的排序（按入驻日期）的值
    :return 日期的前8位变成数字(int或者long)
    """
    return int(datetime.datetime.now().strftime('%Y%m%d'))

def object2dict(obj):
    #convert object to a dict
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d

def dict2object(d):
    #convert dict to object
    if'__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
        inst = class_(**args) #create new instance
    else:
        inst = d
    return inst
