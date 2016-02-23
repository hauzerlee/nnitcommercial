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
