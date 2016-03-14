#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
和用户相关的操作，都定义在这个dao中
"""

import json

import redis
import redis.client

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
        :return boolean True:存在；False：不存在
        """
        is_exist = self.redis.sismember(Constant.MEMBER_USED_CELL_PHONE, cell_phone_number)
        return is_exist

    def get_member_id_by_cell_phone(self, cell_phone_number):
        """
        根据手机号码转化为member ID
        :param cell_phone_number:
        :return:
        """
        return self.redis.hget(Constant.MEMBER_CELL_PHONE, cell_phone_number)

    def auth_session_id(self,member_id, session_id):
        """
        看看这个session是否是上次登陆的
        :param member_id
        :param session_id
        :return: true 或者 false
        """
        key_name = Constant.MEMBER + Constant.COLON + member_id.decode('utf-8') # Sample -> Member:gST8epDEBF8ep4xdcJcGo2
        old_session_in_sys = self.redis.hmget(key_name,"session_id")[0].decode('utf-8')
        if old_session_in_sys:
            return old_session_in_sys==session_id
        else:
            return True

    def login(self, cell_phone_number):
        """
        用户登录，把数据存在Redis中。
        如果用户存在，就返回用户个人信息
        否则，返回一个空的json对象
        :param cell_phone_number: 用户手机号码
        :return 一个json对象
        """
        return_result = {}
        is_exist = self.cell_phone_number_exist(cell_phone_number)
        if is_exist:
            member_id = self.get_member_id_by_cell_phone(cell_phone_number)
            # 用户存在，直接放在Redis的对象中
            session_id = utils.SessionGenerator.session_generate()
            key_name = Constant.MEMBER + Constant.COLON + member_id.decode('utf-8') # Sample -> Member:gST8epDEBF8ep4xdcJcGo2
            self.redis.hmset(key_name, {'session_id': str(session_id)})
            # return_result = {}
            return_result["member_id"] = member_id.decode('utf-8')
            return_result["session_id"] = session_id
            return return_result
        else:
            return_result["member_id"] = ""
            return_result["session_id"] = ""
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
        print(self.redis.smembers(redis_structure_name))
        shop_ids = self.redis.smembers(redis_structure_name)  # 得到收藏的店铺id列表
        shops = []
        index = 0
        # 开始提取店铺的详细信息
        for shop_id in shop_ids:
            key = Constant.SHOP + Constant.COLON + shop_id.decode('utf-8')
            shop = self.redis.hgetall(key)
            shop_tmp = {}
            for (key, value) in shop.items():
                shop_tmp[key.decode('utf-8')] = value.decode('utf-8')
            shops.insert(index, shop_tmp)
            # shops.insert(index, shop)
            index += 1
        shops_map = {}
        shops_map[Constant.JSON_HEAD_SHOPS] = shops
        return shops_map

    def fetch_favors_in_range(self, member_id, page_number):
        """
        随机返回一定数量的收藏商铺
        :param member_id:
        :param quantity_per_page:
        :return 一个店铺的列表（json格式，也是一个小map）
        """
        redis_structure_name = Constant.FAVORS + Constant.COLON + member_id
        shop_ids = self.redis.srandmember(redis_structure_name, Constant.QUANTITY_PER_PAGE * page_number)
        shops = []
        index = 0
        # 开始提取店铺的详细信息
        for shop_id in shop_ids:
            shop_raw = self.redis.hgetall(Constant.SHOP + Constant.COLON + shop_id.decode('utf-8'))
            shop = {}
            for key, value in shop_raw.items():
                shop[key.decode('utf-8')] = value.decode('utf-8')
            shops.insert(index, shop)
            index += 1
        shops_map = {}
        shops_map[Constant.JSON_HEAD_SHOPS] = shops
        return shops_map

    def remove_favor(self, member_id, shop_id):
        """
        删除收藏
        :param member_id
        :param shop_id
        :return 无
        """
        redis_structure_name = Constant.FAVORS + Constant.COLON + member_id
        has_this_favor = self.redis.sismember(redis_structure_name, shop_id)
        removeCount = 0
        if has_this_favor:
            # 从用户自己的队列中删除收藏的shop id
            removeCount = self.redis.srem(redis_structure_name, shop_id)
        return removeCount

    def fetch_groupons(self, member_id):
        """
        提取用户的优惠券
        :param member_id:
        :return：
        """
        redis_structure_name = Constant.GROUPON + Constant.COLON + member_id
        groupon_ids = self.redis.smembers(redis_structure_name)
        groupons = []
        index = 0
        for groupon_id in groupon_ids:
            groupon = self.redis.hgetall(Constant.GROUPON + Constant.COLON + groupon_id.decode('utf-8'))
            g = {}
            for key, value in groupon.items():
                g[key.decode('utf-8')] = value.decode('utf-8')
            groupons.insert(index, g)
            index += 1
        return groupons

    def use_groupon(self, member_id, coupon_id):
        """
        使用一个coupon，直接从用户的redis列表中删除
        :param member_id:
        :param coupon_id:
        :return 无
        """
        redis_structure_name = Constant.GROUPON + Constant.COLON + member_id
        has_this_coupon = redis.SISMEMBER(redis_structure_name, coupon_id)
        if has_this_coupon:
            # 从用户自己的队列中删除已经使用的Coupon Id
            self.redis.srem(redis_structure_name, coupon_id)

    def get_groupon_by_id(self, coupon_id):
        """
        得到一个优惠券的详细信息
        :param coupon_id:
        :return: 优惠券的map
        """
        result = {}
        redis_structure_name = Constant.DISCOUNT + Constant.COLON + coupon_id
        coupon = redis.hgetall(redis_structure_name)
        for (key, value) in coupon.items():
            result[key.decode('utf-8')] = value.decode('utf-8')
        return result

    def get_current_integral(self, member_id):
        """
        提取APP用户当前可用积分
        :param member_id 用户的member ID
        :return: 积分数值
        """
        integral_key = Constant.INTEGRAL + Constant.COLON + member_id.decode('utf-8')
        return int(self.redis.get(integral_key))

    def clear_integral(self, member_id):
        """
        把用户的积分清零
        :param member_id:
        :return:
        """
        integral_key = Constant.INTEGRAL + Constant.COLON + member_id
        self.redis.set(integral_key, 0)

    def save_or_update_integral(self, member_id, increase):
        """
        更新用户的积分
        :param member_id: 用户的ID
        :param increase:  新增的积分数
        :return:
        """
        current_integral = self.get_current_integral(member_id)
        integral_key = Constant.INTEGRAL + Constant.COLON + member_id
        if current_integral:
            increase = increase + int(current_integral)
        # 存入redis中
        return self.redis.set(integral_key, increase)

    def save_groupon_trx(self, member_id, groupon_id):
        """
        用户消费一个团购,需要记录这笔交易

        :param member_id:
        :param groupon_id:
        :return:
        """
        groupon = self.redis.hgetall(Constant.GROUPON + Constant.COLON + groupon_id)
        # 用户的团购交易结构
        redis_key = Constant.MEMBER + Constant.COLON + member_id + Constant.COLON + Constant.GROUPON + Constant.GROUPON_ORDERS  # Member:gST8epDEBF8ep4xdcJcGo2:Groupon:Orders
        trx = {}
        trx["id"] = utils.PrimaryIDGenerator.primary_id_generator()
        trx["groupon_id"] = groupon("ID")
        self.redis.sadd(redis_key, trx) #交易记录


    def get_discount_by_id(self, discount_id):
        """
        提取折扣的详细信息
        :param discount_id:
        :return:
        """
        key_str = "Discount" + Constant.COLON + discount_id
        discount_tmp = self.redis.hgetall(key_str)
        discount = {}
        for (key, value) in discount_tmp.items():
            discount[key.decode('utf-8')] = value.decode('utf-8')
        shop_id = discount['SHOP_ID']
        shop_key_str = "Shop:" + shop_id
        shop_tmp = self.redis.hgetall(shop_key_str)
        shop = {}
        for (key, value) in shop_tmp.items():
            shop[key.decode('utf-8')] = value.decode('utf-8')
        discount["SHOP"] = shop
        return discount

    def fetch_discounts(self, member_id):
        """
        提取某一个用户所具有的折扣
        返回一个折扣的列表
        :param member_id:
        :return:
        """

        key_str = "Discount" + Constant.COLON + member_id
        discount_ids = self.redis.smembers(key_str)
        discounts = []
        index = 0
        for discount_id in discount_ids:
            discounts.insert(index, self.get_discount_by_id(discount_id.decode('utf-8')))
            index += 1
        return discounts

    def use_discount(self, member_id, discount_id):
        """

        :param member_id:
        :param discount_id:
        :return:
        """

        key_str = "Discount" + Constant.COLON + member_id
        has_this_discount = self.redis.sismember(key_str, discount_id)
        if has_this_discount:
            return self.redis.srem(key_str, discount_id)
        else:
            return 0


class UserNotExistException(object):
    def __init__(self):
        pass
