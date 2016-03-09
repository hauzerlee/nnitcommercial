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

SHOP = 'Shop'

#提取商铺的方式
FETCH_SHOP_TYPE_DEFAULT='GRADE' # 评分排序方式
FETCH_SHOP_TYPE_JOIN_DATE = "JOINED_DATE" # 根据商铺加入方式

MEMBER = 'Member'
MEMBER_CELL_PHONE = 'Member:cellphone'
MEMBER_USED_CELL_PHONE = 'Member:used_cellphone'
FAVORS = 'Favors'
INTEGRAL = 'Integral'

HOT_GROUPONS = 'Hot_Groupons'
GROUPON = 'Groupon'
GROUPONS = "Groupons"
GROUPON_ORDERS = "Orders"
DISCOUNTS_SORT = 'Discounts:discountSort'
DISCOUNT = 'Discount'

AUTHORIZATION = 'Authorization'

#JSON列表的key
JSON_HEAD_SHOPS = "shops"
JSON_HEAD_DISCOUNTS = "discounts"
JSON_HEAD_PRODUCTS = "products"
JSON_HEAD_GROUPS = "groups"
JSON_HEAD_TRXS = "trx"

#每页显示的数量
QUANTITY_PER_PAGE = 10