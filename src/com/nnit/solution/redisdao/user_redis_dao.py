#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
和用户相关的操作，都定义在这个dao中
"""

import redis
from com.nnit.solution.local.util import utils


class UserRedisDAO(object):

    def __init__(self):
        # get the redis connection
        self.redis = utils.RedisConnection.get_redis_connection()

    """
    判断用户的手机号码是否已经被使用

    返回：Integer
    """
    def cell_phone_number_exist(self, cell_phone_number):
        redis_structure_name = "Member:cellphone"
        is_exist = redis.sismember(redis_structure_name, cell_phone_number)
        return is_exist

    """
    用户登录，把数据存在Redis中。
    方法要么返回True，要么抛出用户不存在异常

    返回：True或者False
    """
    def login(self, cell_phone_number):
        redis_structure_name = "Member:" + cell_phone_number
        is_exist = self.cell_phone_number_exist(cell_phone_number)
        if is_exist == 0:
            raise UserNotExistException
        # 用户存在，直接放在Redis的对象中
        redis.sadd(redis_structure_name, cell_phone_number)
        return True


    """
    用户注册使用的方法， 通过一个不定长的参数，来存放用户填入的内容

    返回：用户注册的个人信息
    """
    def enrol(self, cell_phone_number, pwd):
        # not exist the cell phone, can go on enrol
        is_exist = self.cell_phone_number_exist(cell_phone_number)
        if is_exist != 0 :
            # TODO(JIAS): put the new user object into 'Member:memberId' redis object
            redis_structure_name = "Member:" + cell_phone_number
            redis.hmset(redis_structure_name, "CELL_PHONE", cell_phone_number)
            redis.hmset(redis_structure_name, "PASSWORD", pwd)
            # generate session id
            # TODO(JIAS): SessionId应该一到MySQL的DAO中处理，然后存储到Redis中
            session_id = utils.SessionGenerator.session_generate()
            redis.hmset(redis_structure_name, "SESSION_ID", session_id)

    """
    更新用户的信息到Redis中
    """
    def update_user(self, user):
        redis_structure_name = "Member:" + user.get_member_id()
        # update the session id
        redis.hmset(redis_structure_name, "SESSION_ID", user.session_id)

    """
    把喜爱的商铺放到收藏夹
    """
    def add_favor(self, member_id, shop_id):
        redis_structure_name = "Favors:" + member_id
        redis.sadd(redis_structure_name, shop_id)

    """
    随机返回全部收藏商铺
    """
    def fetch_favors(self, member_id):
        redis_structure_name = "Favors:" + member_id
        return redis.smembers(redis_structure_name)

    """
    随机返回一定数量的收藏商铺

    返回： 一个list
    """
    def fetch_favors(self, member_id, quantity_per_page):
        redis_structure_name = "Favors:" + member_id
        return redis.srandmember(redis_structure_name, quantity_per_page)

    """
    提取用户的优惠券

    返回：优惠券列表(IDs)
    """
    def fetch_coupons(self, member_id):
        redis_structure_name = "Couponbackage:" + member_id
        return redis.smembers(redis_structure_name)

    """
    提取用户的收藏店铺

    返回：收藏的商铺列表(IDs)
    """
    def fetch_favors(self, member_id):
        redis_structure_name = "Favors:" + member_id
        return redis.smembers(redis_structure_name)


class UserNotExistException(object):

    def __init__(self):
        pass