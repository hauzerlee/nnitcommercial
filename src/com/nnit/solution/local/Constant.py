#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
系统用到的常量，都定义在这里
"""

import sys


class Constant(object):

    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            raise ConstantError
        else:
            self.__dict__[key] = value

    def __getattr__(self, key):
        if self.__dict__.has_key(key):
            return self.key
        else:
            return None


class ConstantError(TypeError):
        def __init__(self):
            pass

# 排序方式
SEARCHING_DIRECTION_ASC = 'asc'
SEARCHING_DIRECTION_DESC = 'desc'

# Redis的Key的前缀
COLON = ":"

LONIN_MEMBERS = 'Login:members'

SHOP = 'Shop:'

MEMBER = 'Member:'
MEMBER_CELL_PHONE = 'Member:cellphone'
FAVORS = 'Favors:'
COUPON_BACKAGE = 'Couponbackage:'
INTEGRAL = 'Integral:'

HOT_GROUPONS = 'Hot_Groupons'
DISCOUNTS_SORT = 'Discounts:discountSort'
DISCOUNT = 'Discount:'

sys.modules[__name__]=Constant()