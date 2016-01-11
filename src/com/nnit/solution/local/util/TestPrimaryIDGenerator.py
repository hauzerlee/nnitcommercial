#!/usr/bin/python3
# Coding:utf-8

# Author: jias
#   Date: 2016.01.11

"""
The tester for utils.py
"""

import unittest


class TestPrimaryIDGenerator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_primary_id_generator(self):

        uuid_str = PrimaryIDGenerator.primary_id_generator()
        print("uuid is %s" % uuid_str)
        self.assertEquals(36, uuid_str.length())

if __name__ == '__main__':
    unittest.main()