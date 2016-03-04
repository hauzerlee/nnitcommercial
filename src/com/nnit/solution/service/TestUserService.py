import unittest
import http.client as httplib
import urllib.parse as urllib
import json


class TestUserService(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_enrol(self):
        cell_phone_num = "13612077384"
        password = "123456"
        params = urllib.urlencode({'cell_phone_num':cell_phone_num, 'password':password})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn = httplib.HTTPConnection("localhost:8888")
        conn.request('POST', '/shoppingmall/members/enrol', params, headers)

        resp = conn.getresponse()
        data = resp.read()
        if resp.status == 200:
            json_data = json.loads(data.decode('utf-8'))
            print(json_data)
        else:
            print(data)

    def test_login(self):
        cell_phone_num = '13612077384'
        params = urllib.urlencode({'cell_phone_num':cell_phone_num})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn = httplib.HTTPConnection("localhost:8888")
        conn.request('POST', '/shoppingmall/members/login', params, headers)

        resp = conn.getresponse()
        data = resp.read()
        if resp.status == 200:
            json_data = json.loads(data.decode('utf-8'))
            print(json_data)
        else:
            print(data)

    def test_remove_favor_shop(self):
        member_id = 'gST8epDEBF8ep4xdcJcGo2'
        shop_id = 'kQNbn6HQproeUGkZSKBAkf'
        params = urllib.urlencode({'member_id':member_id, "shop_id":shop_id})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn = httplib.HTTPConnection("localhost:8888")
        conn.request('POST', '/shoppingmall/favours/member/shop/remove', params, headers)

        resp = conn.getresponse()
        data = resp.read()
        if resp.status == 200:
            print("success -> ")
            print(data)
        else:
            print("  fail --> " )
            print(data)