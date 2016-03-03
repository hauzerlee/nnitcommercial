#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.02.21

import os

import pyrestful.rest
import tornado.ioloop

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

from com.nnit.solution.service import UserService

# a list to route different REST Service.
restservices = []
restservices.append(UserService.MemberServices)
if __name__ == "__main__":

    try:
        app = pyrestful.rest.RestService(restservices)
        port = 8889
        app.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except Exception:
        pass
