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

Constant.SEARCHING_DIRECTION_ASC = 'asc'
Constant.SEARCHING_DIRECTION_DESC = 'desc'

sys.modules[__name__]=Constant()