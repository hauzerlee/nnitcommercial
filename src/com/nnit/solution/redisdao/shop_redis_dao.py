#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.18

"""
和商户相关的操作，都定义在这个dao中
"""

import sys
import redis
import json
from com.nnit.solution.local import Constant
from com.nnit.solution.local.util import utils


class ShopRedisDAO(object):

    def __init__(self):
        # get the redis connection
        self.redis = utils.RedisConnection.get_redis_connection()


    def save_or_update(self, shop_json_str='', shop_obj = None):
        """
        保存或者更新一个shop对象
        这个shop对象，必须已经保存到了MySQL中。 对应的ID必须已经生成
        :param shop_json_str : 可以传入json串作为shop的数据，默认是一个空字符串
        :param shop_obj      : shop的对象实例，默认是一个None
        """
        if shop_json_str.strip():
            shop = json.loads(shop_json_str)

        if shop_obj is not None:
            shop = shop_obj

        redis_key = Constant.SHOP + Constant.COLON + shop.ID
        shop_mapping = {"ID":shop.ID, "SHOP_NAME":shop.name, "FLOOR": shop.floor,
                        "LOCATION":shop.location, "LOGO":shop.logo, "TRUE_SCENE":shop.true_scene,
                        "TELEPHONE":shop.telephone, "CONTACT":shop.contact, "CONTACT_TEL":shop.contact_tel,
                        "INTRODUCTION":shop.introduction, "CATEGORY_ID":shop.category_id,
                        "CREATE_TIME":shop.create_time, "OPENING_TIME":shop.opening_time,
                        "MEMBER_ID": shop.member_id}
        self.redis.hmset(redis_key, shop_mapping)

        #把商铺放到2个zset中（暂时只有2个），用于提取商品列表
        # score
        redis_key = Constant.SHOP + Constant.COLON + Constant.FETCH_SHOP_TYPE_DEFAULT
        self.redis.zadd(redis_key,shop.ID, 3) # 默认给3分
        # join_date
        redis_key = Constant.SHOP + Constant.COLON + Constant.FETCH_SHOP_TYPE_DEFAULT
        self.redis.zadd(redis_key,shop.ID, utils.getDatetToLong())


    def get_shop_by_id(self, shop_id):
        """
        根据ID提取一个店铺的全部信息，返回一个JSon对象
        如果没有传入shop_id，或者是一个无效的shop_id，返回一个空的json
        :param shop_id:  店铺的ID
        :return shop info
        """
        result = {}
        if shop_id.strip(): # 如果shop_id不为空
            redis_key = Constant.SHOP + Constant.COLON + shop_id
            shop_info = self.redis.hgetall(redis_key)
            for (key, value) in shop_info.items():
                result[key.decode('utf-8')] = value.decode('utf-8')
        return result

    def get_shops(self, fetch_type=Constant.FETCH_SHOP_TYPE_DEFAULT, start=0, end=9):
        """
        得到一个商铺列表（一般一屏能显示的数量是10)
        :param fetch_type: 提起商铺的方式。默认采用商铺的评分方式
        :param start : 开始的位置
        :param end :   结束的位置
        返回：json对象
        """
        redis_key = Constant.SHOP + ":" + fetch_type
        shop_ids = self.redis.zrevrange(redis_key,start, end, withscores=False)
        # 遍历每个id，提取每个shop的详细信息，并放到一个json里
        shops_list = []
        for id in shop_ids:
            r_key = Constant.SHOP + Constant.COLON + id
            shops_list.append(json.dump(self.redis.hgetall(r_key)))
        shops = {Constant.JSON_HEAD_SHOPS:shops_list}
        return json.dump(shops)


    # -----------------------------------------------------------------------
    # 商户发布信息的方法
    # -----------------------------------------------------------------------

    def create_groupon(self, shop_id, groupon, groupon_json=""):
        if (groupon_json != "" and groupon == None):
            groupon = json.load(groupon_json)
        # 采用groupon来操作
        redis_key_discount = Constant.GROUPON + Constant.COLON + utils.PrimaryIDGenerator.primary_id_generator()
        groupon_mapping = {"ID":groupon.ID, "SHOP_ID":groupon.shop_id, "TITLE":groupon.title, "PICTURE":groupon.picture,
                           "ORIGINAL_PRICE":groupon.original_price,"CURRENT_PRICE":groupon.current_price,
                           "START_TIME":groupon.start_time, "END_TIME":groupon.end_time,
                           "DETAILS":groupon.details,"CREATE_TIME":groupon.create_time}
        self.redis.hmset(redis_key_discount, groupon_mapping)


    def publish_groupons(self, shop_id, groupon_ids):
        """
        商户发布团购信息
        :param shop_id     商铺的id
        :param groupon_ids 需要发布的团购id列表（一个list）
        """
        # 依次加入到zset里，并根据serialNum自动排序
        for groupon_id in groupon_ids:
            serial_num = utils.SortedValueGenerator.generate_releaseDateValue() + shop_id * 10
            self.redis.zadd(Constant.HOT_GROUPONS, groupon_id, serial_num)

    def publis_discounts(self, shop_id, discount_ids_map, discount_values_map):
        """
        商户发布折扣信息
        (貌似管理平台需要传入很多参数。需要和Oliver协商)
        :param: shop_id      商铺的id
        :param: discount_ids 需要发布的折扣id列表（一个map）
                            key: production_id
                            value: discount_id
        :param: discount_values 需要发布的折扣的值（一个map）
                            key: production_id
                            value: discount_value
        """
        # 依次加入到zset里，并根据serialNum自动排序
        for production_id in discount_ids_map:
            """ 创建一个折扣的redis对象 """
            """ key是 Discount:discountId """
            redis_key_discount = Constant.DISCOUNT + Constant.COLON + discount_ids_map[production_id]
            self.redis.hmset(redis_key_discount, production_id, discount_values_map[production_id])

            """ 放到公共的redis折扣列表里 """
            self.redis.hmset(Constant.DISCOUNTS_SORT,
                             discount_ids_map[production_id],
                             discount_values_map[production_id])

    # -----------------------------------------------------------------------
    # 用户提取折扣、优惠券信息
    # -----------------------------------------------------------------------


    def get_available_discounts(self):
        """
        用户从移动终端提取目前热门的折扣信息
        """
        return self.redis.smembers(Constant.DISCOUNTS_SORT)


    def get_available_groupons(self):
        """
        用户从移动终端提取目前热门的团购信息
        """
        return self.redis.smembers(Constant.HOT_GROUPONS)
