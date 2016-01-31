#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
和用户相关的操作，都定义在这个dao中
"""

import redis
from com.nnit.solution.local.util import utils
from com.nnit.solution.local import Constant


class UserRedisDAO(object):
    def __init__(self):
        # get the redis connection
        self.redis = utils.RedisConnection.get_redis_connection()

    """
    判断用户的手机号码是否已经被使用
    这是一个“手机号码”和“用户id”的映射

    返回：Integer
    """

    def cell_phone_number_exist(self, cell_phone_number):
        is_exist = self.redis.sismember(Constant.MEMBER_USED_CELL_PHONE, cell_phone_number)
        return is_exist

    """
    用户登录，把数据存在Redis中。
    方法要么返回True，要么抛出用户不存在异常

    返回：True或者False
    """

    def login(self, cell_phone_number):
        is_exist = self.cell_phone_number_exist(cell_phone_number)
        if is_exist == 0:
            raise UserNotExistException
        member_id = self.redis.hget(Constant.MEMBER_CELL_PHONE, cell_phone_number)
        # 用户存在，直接放在Redis的对象中
        session_id = utils.SessionGenerator.session_generate()
        key_name = Constant.MEMBER + member_id.decode('utf-8')
        self.redis.hmset(key_name, {'SESSION_ID': session_id})
        return True

    """
    用户注册使用的方法， 通过一个不定长的参数，来存放用户填入的内容

    返回：用户注册的个人信息
    """

    def enrol(self, cell_phone_number, pwd):
        # not exist the cell phone, can go on enrol
        is_exist = self.cell_phone_number_exist(cell_phone_number)
        if is_exist != 0:
            # Generate the member's primary ID
            member_id = utils.PrimaryIDGenerator.primary_id_generator()
            # TODO(JIAS): put the new user object into 'Member:memberId' redis object
            redis_structure_name = Constant.MEMBER + member_id
            # TODO(JIAS): SessionId应该一到MySQL的DAO中处理，然后存储到Redis中
            session_id = utils.SessionGenerator.session_generate()
            values = {'CELL_PHONE': cell_phone_number, 'PASSWORD': pwd, 'ID': member_id, 'SESSION_ID': session_id}
            self.redis.hmset(redis_structure_name, values)

            # 把号码放置到Member:cellphone中，标识此号码已经被注册过了
            self.redis.hset(Constant.MEMBER_CELL_PHONE, cell_phone_number, member_id)
            self.redis.sadd(Constant.MEMBER_USED_CELL_PHONE, cell_phone_number)

    """
    更新用户的信息到Redis中
    """

    def update_user(self, user):
        redis_structure_name = Constant.MEMBER + user.get_member_id()
        # update the session id
        redis.hmset(redis_structure_name, "SESSION_ID", user.session_id)

    """
    把喜爱的商铺放到收藏夹
    """

    def add_favor(self, member_id, shop_id):
        redis_structure_name = Constant.FAVORS + member_id
        redis.sadd(redis_structure_name, shop_id)

    """
    随机返回全部收藏商铺
    """

    def fetch_favors(self, member_id):
        redis_structure_name = Constant.FAVORS + member_id
        return redis.smembers(redis_structure_name)

    """
    随机返回一定数量的收藏商铺

    返回： 一个list
    """

    def fetch_favors_in_range(self, member_id, quantity_per_page):
        redis_structure_name = Constant.FAVORS + member_id
        return redis.srandmember(redis_structure_name, quantity_per_page)

    """
    提取用户的收藏店铺

    返回：收藏的商铺列表(IDs)
    """

    def fetch_favors(self, member_id):
        redis_structure_name = Constant.FAVORS + member_id
        return redis.smembers(redis_structure_name)

    """
    删除收藏

    返回：无
    """

    def remove_favor(self, member_id, shop_id):
        redis_structure_name = Constant.FAVORS + member_id
        has_this_favor = redis.SISMEMBER(redis_structure_name, shop_id)
        if has_this_favor == 1:
            # 从用户自己的队列中删除收藏的shop id
            redis.SREM(redis_structure_name, shop_id)

    """
    提取用户的优惠券

    返回：优惠券列表(IDs)
    """

    def fetch_coupons(self, member_id):
        redis_structure_name = Constant.COUPON_BACKAGE + member_id
        return redis.smembers(redis_structure_name)

    """
    使用一个coupon，直接从用户的redis列表中删除

    返回： 无
    """

    def use_coupon(self, member_id, coupon_id):
        redis_structure_name = Constant.COUPON_BACKAGE + member_id
        has_this_coupon = redis.SISMEMBER(redis_structure_name, coupon_id)
        if has_this_coupon == 1:
            # 从用户自己的队列中删除已经使用的Coupon Id
            redis.SREM(redis_structure_name, coupon_id)


class UserNotExistException(object):
    def __init__(self):
        pass
