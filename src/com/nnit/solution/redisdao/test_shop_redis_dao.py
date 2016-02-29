#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16


import unittest
import json
from com.nnit.solution.local.util import utils
from com.nnit.solution.local import Constant
from com.nnit.solution.redisdao import shop_redis_dao
from com.nnit.solution.entity import entitys


class TestShopRedisDAO(unittest.TestCase):

    def setUp(self):
        self.redis = utils.RedisConnection.get_redis_connection()

    def tearDown(self):
        pass

    def test_publish_groupons(self):
        print("-------------------------")
        print('execute test_publish_groupons() ')
        shop_dao = shop_redis_dao.ShopRedisDAO()
        ''' Prepare testing data '''
        shop_id = 1
        groupon_ids = [1, 2, 3]
        shop_dao.publish_groupons(shop_id, groupon_ids)
        ''' doing testing '''
        ids = self.redis.zrange(Constant.HOT_GROUPONS, 0, -1)
        for id in ids:
            print(id)
        print("-------------------------")
        id_and_score = self.redis.zrangebyscore(Constant.HOT_GROUPONS, 0, 99999999999, withscores=True)
        for id_score in id_and_score:
            print(id_score)
        print("-------------------------")
        self.redis.zrem(Constant.HOT_GROUPONS, 1, 2, 3)

    def test_publis_discounts(self):
        print("-------------------------")
        print('execute test_publis_discounts() ')
        shop_dao = shop_redis_dao.ShopRedisDAO()
        ''' Prepare testing data '''
        shop_id = 1
        discounts = [1, 2, 3]
        shop_dao.publis_discounts(shop_id, discounts)
        ''' doing testing '''
        ids = self.redis.zrange(Constant.DISCOUNTS_SORT, 0, -1)
        for id in ids:
            print(id)
        print("-------------------------")
        id_with_score = self.redis.zrangebyscore(Constant.DISCOUNTS_SORT, 0, 99999999999, withscores=True)
        for id_score in id_with_score:
            print(id_score)
        print("-------------------------")
        self.redis.zrem(Constant.DISCOUNTS_SORT, 1, 2, 3)

    def test_create_groupon(self):
        """
        测试创建一个团购
        :return:
        """
        groupon_json = "{ID:12345, SHOP_ID:23456, TITLE:TEST_GROUPON, PICTURE:HTTP://WWW.ABC.IO/PIC1.JPGE," \
                       " ORIGINAL_PRICE:100.00, CURRENT_PRICE:50.00, START_TIME:9:00, END_TIME:19:00, DETAILS:THIS IS A TESTING GROUPON, " \
                       " CREATE_TIME:2016-01-01 12:32:23}"
        # groupon = json.loads(groupon_json, object_hook = utils.dict2object)
        # print(groupon)
        # print(groupon.SHOP_ID)

    def test_get_shop_by_id(self):
        shop_dao = shop_redis_dao.ShopRedisDAO()
        print(shop_dao.get_shop_by_id("bsuE9msdeALT4ZhfyXRTRo"))

    def test_save_or_update(self):
        shop_dao = shop_redis_dao.ShopRedisDAO()
        shop_json = {"ID":"bsuE9msdeALT4ZhfyXRTRo","shop_name":"周大福","floor":"1F","location":"33号",
                     "logo":"http://www.bac.org/logo.jpeg","true_scene":"http://www.bac.org/true_scene.jpeg",
                     "telephone":"87282928","contact":"周大福","contact_tel":"1365935698",
                     "introduction":"周大福珠宝金行由周至元先生于1929年广州市创立，其后迁往澳门，于1939年正式在香港成立。1956年，周大福由郑裕彤先生接手经营，始创999.9纯金首饰，成为今日首饰行业黄金成色的香港标准。",
                     "category":"1","create_time":"2016-02-28 12:34:43","opening_time":"2015-12-01-01","member":"gST8epDEBF8ep4xdcJcGo2"}

        shop_dao.save_or_update(shop_json)
        print("test_save_or_update -> ")
        print(shop_dao.get_shop_by_id('bsuE9msdeALT4ZhfyXRTRo'))