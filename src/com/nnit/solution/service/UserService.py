#!/usr/bin/python3
# Coding:utf-8

# Author: JIAS
#   Date: 2016.01.16

"""
APP、 后台管理系统，与用户相关的操作，都定义在这个Service中
"""

import pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get
from pyrestful.rest import post

from com.nnit.solution.local.util import utils
from com.nnit.solution.redisdao import user_redis_dao


class MemberServices(pyrestful.rest.RestHandler):
    """
    返回用户的个人信息
    """

    # REST-GET
    @get(_path="/shoppingmall/members/{member_id}", _produces=mediatypes.APPLICATION_JSON)
    def get_member_info(self, member_id):
        redis_dao = user_redis_dao.UserRedisDAO()
        return redis_dao.getMemberInfo(member_id)

    # REST-POST
    @post(_path="/shoppingmall/members/login", _types=[bytes], _produces=mediatypes.APPLICATION_JSON)
    def login(self, cell_phone_num):
        """
        这个方法适用于用户已经重手机端登出，
        APP需要用户提供预设密码
        先看Redis中是否有对应的对象，
        如果有，直接从Redis中
        返回用户的信息，并生成新的SessionId，更新redis数据
        如果没有，从MySQL中提取数据，
        并更新redis的数据

        返回：用户的个人信息
        """
        print("cell_phone_num -> " + cell_phone_num)
        return user_redis_dao.UserRedisDAO.login(cell_phone_num)

    # REST-POST
    @post(_path="/shoppingmall/members/enrol", _types=[bytes, bytes], _produces=mediatypes.APPLICATION_JSON)
    def enrol(self, cell_phone_num, password):
        print("cell_phone_num -> " + cell_phone_num)
        enrol_result = {"status":False, "memberId":'', "sessionId":''}
        # enrol_result["status"] = False
        # enrol_result["memberId"] = ""
        # enrol_result["sessionId"] = ""
        if cell_phone_num is not None:
            redis_dao = user_redis_dao.UserRedisDAO()
            result = redis_dao.enrol(cell_phone_num, password)
            if result:
                # enrol_result["status"] = True
                # enrol_result["memberId"] = result[0]
                # enrol_result["sessionId"] = result[1]
                enrol_result = {"status":True, "memberId":result[0], "sessionId": result[1]}
        return enrol_result

    # REST-POST
    @post(_path="", _produces=mediatypes.APPLICATION_JSON)
    def login_directly(self, cell_phone_num, session_id):
        """
        这个方法适用于用户没有从APP中登出，在APP中存在一个
        上次登录时的SessionID
        登录逻辑同login()方法基本相同。
        唯一的不同，就是不需要验证用户的密码，而是去验证用户
        上次登录时生成的SessionId

        返回：用户的个人信息
        """
        try:
            isEnrol = user_redis_dao.UserRedisDAO.login(cell_phone_num)
            if isEnrol:
                new_session_id = utils.SessionGenerator.session_generate()
                user = user_redis_dao.UserRedisDAO.get_user_by_phone_number(cell_phone_num)
                if session_id == user.get_session_id():  # 用户终端存在sessionId，没有”登出“
                    user.set_session_id(new_session_id)
                    user_redis_dao.UserRedisDAO.update_user(user)  # update in redis
                    # --------------------------------------
                    # TODO(JIAS): 更新MySQL中用户的sessionId
                    # --------------------------------------
                    return user  # 返回用户对象
                else:
                    return  # 没有注册过；或者已经“登出”
        except user_redis_dao.UserNotExistException:
            print('User NOT Exist Exception')

    # REST-GET
    @get(_path="/shoppingmall/members/integral/{cell_phone_num}", _products=mediatypes.APPLICATION_JSON)
    def get_current_integral(self, cell_phone_num):
        """
        :param cell_phone_num 用户的手机号码
        :return 用户当前可用的积分总数
        """
        member_id = user_redis_dao.UserRedisDAO.get_member_id_by_cell_phone(cell_phone_num)
        if member_id:
            return user_redis_dao.UserRedisDAO.get_current_integral(member_id)
        return 0




"""
通过用户的UUID来提取优惠券

返回一个优惠券的列表
"""


def fetch_coupons(self, member_id):
    coupons = user_redis_dao.UserRedisDAO.fetch_coupons(member_id)
    pass


"""
提取某个类型的优惠券

返回一个优惠券的列表
"""


def fetch_coupons_with_type(self, member_id, coupon_type):
    pass


def fetch_favor(self, member_id):
    pass


"""
用户修改密码

返回True或者False
"""


def change_password(self, old_pwd, new_pwd, confirm_new_pwd):
    if new_pwd != confirm_new_pwd:
        return False
    pass


"""
用户登出

返回True或者False
"""


def log_out(self, member_id):
    pass


"""
查询会员积分

返回一个Integer
"""


def watch_integral_balance(self, member_id):
    pass


"""
提取用户积分交易的记录
根据交易时间倒叙排列返回

返回一个List
"""


def fetch_trx_of_integral(self, member_id):
    pass


"""
未读消息的数量

返回： Integer
"""


def new_msg_count(self, member_id):
    redis_key = "Message:new:" + member_id
    return self.redis.scard(redis_key)


"""
获取未读的消息

返回一个消息列表
"""


def new_msgs(self, member_id):
    redis_key = "Message:new:" + member_id
    return self.redis.smember(redis_key)


"""
全部消息的数量

返回： Integer
"""


def msg_count(self, member_id):
    redis_ley = "Message:" + member_id
    return self.redis.scard(redis_ley)


"""
获取全部消息

返回一个消息列表
"""


def new_msgs(self, member_id):
    redis_key = "Message:" + member_id
    return self.redis.smember(redis_key)

