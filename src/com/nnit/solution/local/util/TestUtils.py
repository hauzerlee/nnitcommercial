#!/usr/bin/python3
# Coding:utf-8

# Author: jias
#   Date: 2016.01.11

"""
The tester for utils.py
"""

import unittest
import shortuuid
from com.nnit.solution.local.util import utils
from com.nnit.solution.local import Constant


class TestPrimaryIDGenerator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    '''
    Test the primary id generate for MySQL Primary ID
    '''
    def test_primary_id_generator(self):
        for i in range(1,100):
            uuid_str = utils.PrimaryIDGenerator.primary_id_generator()
            print("first  uuid is %s" % uuid_str)
            self.assertIsNotNone(uuid_str,'Generate UUID failed.')

    '''
    Test the connection create is ok or not
    '''
    def test_get_redis_connection(self):
        host="localhost"
        port=6079
        dbName=""
        redis_conn = utils.RedisConnection.get_redis_connection(host, port,dbName)
        self.assertIsNotNone(redis_conn, 'Create the redis connection fail')

if __name__ == '__main__':
    unittest.main()