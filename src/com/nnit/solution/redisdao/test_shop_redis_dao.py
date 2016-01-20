#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16


import unittest
from com.nnit.solution.local.util import utils
from com.nnit.solution.local import Constant
from com.nnit.solution.redisdao import shop_redis_dao


class TestShopRedisDAO(unittest.TestCase):

    def setUp(self):
        self.redis = utils.RedisConnection.get_redis_connection('localhost', 6379, 0)

    def tearDown(self):
        pass

    def test_publish_groupons(self):
        shop_dao = shop_redis_dao.ShopRedisDAO()
        # Prepare testing data
        shop_id = 1
        groupon_ids = [1, 2, 3]
        shop_dao.publish_groupons(shop_id, groupon_ids)
        # doing testing
        ids = self.redis.zrange(Constant.HOT_GROUPONS, 0, -1)
        for id in ids:
            print(id)
        print("-------------------------")
        id_and_score = self.redis.zrangebyscore(Constant.HOT_GROUPONS, 0, 99999999999, withscores=True)
        for id_score in id_and_score:
            print(id_score)
        print("-------------------------")
        self.redis.zrem(Constant.HOT_GROUPONS, 1, 2, 3)