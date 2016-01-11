#!/usr/bin/python3
# Coding:utf-8

# Author: jias
#   Date: 2016.01.11

"""
All database record need a primary key.
In our system, the primary key is 32bit string
UUID is a good choice for use.

Here is the usage:

uuid_instance = PrimaryIDGenerator.uuid_generator()

"""

import datetime
import uuid


class PrimaryIDGenerator(object):

    @staticmethod
    def primary_id_generator():
        return uuid.uuid1(uuid.getnode(), datetime.datetime.now().microsecond)
