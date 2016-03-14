import unittest

from com.nnit.solution.redisdao import user_redis_dao
from com.nnit.solution.local import Constant


class TestUserRedisDAO(unittest.TestCase):
    userDAO = user_redis_dao.UserRedisDAO()
    cell_phone = '13612077384'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cell_phone_number_exist(self):
        # userDAO = user_redis_dao.UserRedisDAO()
        is_exist = self.userDAO.cell_phone_number_exist(self.cell_phone)
        self.assertEqual(1, is_exist)

    def test_enrol(self):
        pwd = '123456'
        self.userDAO.enrol(self.cell_phone, pwd)
        is_exist = self.userDAO.cell_phone_number_exist(self.cell_phone)
        self.assertEqual(1, is_exist)

    def test_login(self):
        pwd = '123456'
        self.userDAO.enrol(self.cell_phone, pwd)
        result = self.userDAO.login(self.cell_phone)
        self.assertTrue(result)
        is_exist = self.userDAO.cell_phone_number_exist(self.cell_phone)
        self.assertEqual(1, is_exist)

    def test_getMemberInfo(self):
        result = self.userDAO.login(self.cell_phone)
        print("test_getMemberInfo() --- ")
        print(result)
        print(result['memberid'])
        print("--------------------------")
        member = self.userDAO.getMemberInfo(result['memberid'])
        print("test_getMemberInfo() --- ")
        print(member)
        print("--------------------------")
        # result = {}

    def test_get_current_integral(self):
        member_id = 'gST8epDEBF8ep4xdcJcGo2'
        self.userDAO.clear_integral(member_id)
        save_result = self.userDAO.save_or_update_integral(member_id, 100)
        result = self.userDAO.get_current_integral(member_id)
        self.assertEqual(100, result)

    def test_fetch_favors(self):
        member_id = 'gST8epDEBF8ep4xdcJcGo2'
        shops_map = self.userDAO.fetch_favors(member_id)
        shops = shops_map[Constant.JSON_HEAD_SHOPS]
        for shop in shops:
            print(shop)

    def test_list_and_dict(self):
        shops_list = [{"ID": "bsuE9msdeALT4ZhfyXRTRo", "shop_name": "周大福", "floor": "1F", "location": "33号",
                       "logo": "http://www.bac.org/logo.jpeg"},
                      {"ID": "kQNbn6HQproeUGkZSKBAkf", "shop_name": "周小福", "floor": "1F", "location": "33号",
                       "logo": "http://www.bac.org/logo.jpeg"}]
        for shop in shops_list:
            print(shop)
            for (key, value) in shop.items():
                print(key + ":" + value)


    def test_get_discount_by_id(self):
        discount_id = "pvqMYQLdMYohuhRaRSiquX"
        discount = self.userDAO.get_discount_by_id(discount_id)
        print(discount)

    def test_fetch_discounts(self):
        member_id = 'gST8epDEBF8ep4xdcJcGo2'
        print(self.userDAO.fetch_discounts(member_id))

    def test_use_discount(self):
        member_id = 'gST8epDEBF8ep4xdcJcGo2'
        discount_id = 'pvqMYQLdMYohuhRaRSiquX'
        count = self.userDAO.use_discount(member_id,discount_id)
        self.assertEqual(1,count)