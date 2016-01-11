#!/usr/bin/python3
# Coding:utf-8

# Author: jias
#   Date: 2016.01.11

"""
Some global operations need use a single instance
Here defines a singleton supper class, which the sub-classes
inherit this class will only one instance in the running time

Here is the usage:

class MyClass(object):
    __metaclass__ = Singleton

The "MyClass" is a singleton class

"""


class Singleton(type):
    def __init__(cls, name, bases, dictionary):
        super(Singleton, cls).__init__(name, bases, dictionary)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance
