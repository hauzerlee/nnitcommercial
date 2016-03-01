import unittest

from com.nnit.solution.redisdao import user_redis_dao


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
