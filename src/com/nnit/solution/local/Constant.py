#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
系统用到的常量，都定义在这里
"""

import sys

#UUID生成的种子
UUID_SEED = 'http://www.nnit.com/local'


# 排序方式
SEARCHING_DIRECTION_ASC = 'asc'
SEARCHING_DIRECTION_DESC = 'desc'

# Redis的Key的前缀
COLON = ":"

LONIN_MEMBERS = 'Login:members'

SHOP = 'Shop:'

#提取商铺的方式
FETCH_SHOP_TYPE_DEFAULT='GRADE' # 评分排序方式
FETCH_SHOP_TYPE_JOIN_DATE = "JOINED_DATE" # 根据商铺加入方式

MEMBER = 'Member:'
MEMBER_CELL_PHONE = 'Member:cellphone'
MEMBER_USED_CELL_PHONE = 'Member:used_cellphone'
FAVORS = 'Favors:'
COUPON_BACKAGE = 'Couponbackage:'
INTEGRAL = 'Integral:'

HOT_GROUPONS = 'Hot_Groupons'
DISCOUNTS_SORT = 'Discounts:discountSort'
DISCOUNT = 'Discount:'