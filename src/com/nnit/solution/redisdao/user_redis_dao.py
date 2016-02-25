#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
和用户相关的操作，都定义在这个dao中
"""

import json

import redis

from com.nnit.solution.local import Constant
from com.nnit.solution.local.util import utils


class UserRedisDAO(object):
    def __init__(self):
        # get the redis connection
        self.redis = utils.RedisConnection.get_redis_connection()

    def cell_phone_number_exist(self, cell_phone_number):
        """
        判断用户的手机号码是否已经被使用
        这是一个“手机号码”和“用户id”的映射
        :param cell_phone_number: 用户手机号码
        :return Integer
        """
        is_exist = self.redis.sismember(Constant.MEMBER_USED_CELL_PHONE, cell_phone_number)
        return is_exist

    def login(self, cell_phone_number):
        """
        用户登录，把数据存在Redis中。
        方法要么返回True，要么抛出用户不存在异常
        :param cell_phone_number: 用户手机号码
        :return 一个json字符串
        """
        return_result = []
        is_exist = self.cell_phone_number_exist(cell_phone_number)
        if is_exist == 0:
            return_result.append("memberid:")
            return_result.append("session_id:")
            return return_result
        member_id = self.redis.hget(Constant.MEMBER_CELL_PHONE, cell_phone_number)
        # 用户存在，直接放在Redis的对象中
        session_id = utils.SessionGenerator.session_generate()
        key_name = Constant.MEMBER + Constant.COLON + member_id.decode('utf-8')
        self.redis.hmset(key_name, {'SESSION_ID': str(session_id)})
        return_result = []
        return_result.append("memberid:"+ member_id)
        return_result.append("session_id:" + session_id)
        return return_result

    def getMemberInfo(self, member_id):
        """
        返回APP用户的个人信息
        :param member_id: APP用户的ID
        :return: 用户的个人信息 (dict)
        """
        member = self.redis.hgetall(Constant.MEMBER + Constant.COLON + member_id)
        result = {}
        for (key, value) in member.items():
            result[key.decode('utf-8')] = value.decode('utf-8')
        return result  # 应该是一个Map

    def enrol(self, cell_phone_number, pwd):
        """
        用户注册使用的方法， 通过一个不定长的参数，来存放用户填入的内容
        :param cell_phone_number 用户手机号码
        :param pwd 用户密码
        :return 用户注册的个人信息
        """
        enrol_result = []
        # not exist the cell phone, can go on enrol
        is_exist = self.cell_phone_number_exist(cell_phone_number)
        if is_exist:
            return enrol_result
        else:
            # Generate the member's primary ID
            # member = entitys.Member.create(cell_phone_number, password=pwd)
            member_id = utils.PrimaryIDGenerator.primary_id_generator()
            # TODO(JIAS): put the new user object into 'Member:memberId' redis object
            redis_structure_name = Constant.MEMBER + Constant.COLON + member_id
            # TODO(JIAS): SessionId应该一到MySQL的DAO中处理，然后存储到Redis中
            session_id = utils.SessionGenerator.session_generate()
            values = {'CELL_PHONE': cell_phone_number, 'PASSWORD': pwd, 'ID': member_id, 'SESSION_ID': session_id}
            self.redis.hmset(redis_structure_name, values)

            # 把号码放置到Member:cellphone中，标识此号码已经被注册过了
            self.redis.hset(Constant.MEMBER_CELL_PHONE, cell_phone_number, member_id)
            self.redis.sadd(Constant.MEMBER_USED_CELL_PHONE, cell_phone_number)
            enrol_result.append(member_id)
            enrol_result.append(str(session_id))
            return enrol_result

    def update_user(self, member):
        """
        更新用户的信息到Redis中
        :param  member: 用户对象
        """
        redis_structure_name = Constant.MEMBER + Constant.COLON + member.ID
        member_value = {"ID": member.ID, "CELL_PHONE": member.cell_phone, "NICK_NAME": member.nick_name,
                        "PASSWORD": member.password, "SESSION_ID": member.session_id,
                        "LASTEST_LOGIN": member.lastest_login,
                        "ACCOUNT_NUMBER": member.account_number, "GRADE": member.grade, "STATUS": member.status,
                        "IS_ONLINE": member.is_online, "GENDER": member.gender, "PIC": member.pic,
                        "EMAIL_ADDR": member.email_addr, "TYPE": member.type}
        # update the session id
        redis.hset(redis_structure_name, member_value)

    def add_favor(self, member_id, shop_id):
        """
        把喜爱的商铺放到收藏夹
        :param  member_id 用户ID
        :param  shop_id   关注的商铺ID
        :return
        """
        redis_structure_name = Constant.FAVORS + Constant.COLON + member_id
        redis.sadd(redis_structure_name, shop_id)

    def fetch_favors(self, member_id):
        """
        随机返回全部收藏商铺
        :param member_id : 用户ID
        :return 收藏的店铺列表
        """
        redis_structure_name = Constant.FAVORS + Constant.COLON + member_id
        shop_ids = redis.smembers(redis_structure_name)  # 得到收藏的店铺id列表
        shops = []
        index = 0
        # 开始提取店铺的详细信息
        for shop_id in shop_ids:
            shops.insert(index, json.dump(self.redis.hgetall(Constant.SHOP + Constant.COLON + shop_id)))
            index += 1
        shops_map = {Constant.JSON_HEAD_SHOPS: shops}
        return json.dump(shops_map)

    def fetch_favors_in_range(self, member_id, quantity_per_page):
        """
        随机返回一定数量的收藏商铺
        :param member_id:
        :param quantity_per_page:
        :return 一个店铺的列表（json格式，也是一个小map）
        """
        redis_structure_name = Constant.FAVORS + Constant.COLON + member_id
        shop_ids = redis.srandmember(redis_structure_name, quantity_per_page)
        shops = []
        index = 0
        # 开始提取店铺的详细信息
        for shop_id in shop_ids:
            shops.insert(index, json.dump(self.redis.hgetall(Constant.SHOP + Constant.COLON + shop_id)))
            index += 1
        shops_map = {Constant.JSON_HEAD_SHOPS: shops}
        return json.dump(shops_map)

    def remove_favor(self, member_id, shop_id):
        """
        删除收藏
        :param member_id
        :param shop_id
        :return 无
        """
        redis_structure_name = Constant.FAVORS + Constant.COLON + member_id
        has_this_favor = redis.SISMEMBER(redis_structure_name, shop_id)
        if has_this_favor == 1:
            # 从用户自己的队列中删除收藏的shop id
            redis.SREM(redis_structure_name, shop_id)

    def fetch_coupons(self, member_id):
        """
        提取用户的优惠券
        :param member_id:
        :return：优惠券列表(IDs)
        """
        redis_structure_name = Constant.COUPON_BACKAGE + Constant.COLON + member_id
        return redis.smembers(redis_structure_name)

    def use_coupon(self, member_id, coupon_id):
        """
        使用一个coupon，直接从用户的redis列表中删除
        :param member_id:
        :param coupon_id:
        :return 无
        """
        redis_structure_name = Constant.COUPON_BACKAGE + Constant.COLON + member_id
        has_this_coupon = redis.SISMEMBER(redis_structure_name, coupon_id)
        if has_this_coupon == 1:
            # 从用户自己的队列中删除已经使用的Coupon Id
            redis.SREM(redis_structure_name, coupon_id)


class UserNotExistException(object):
    def __init__(self):
        pass
