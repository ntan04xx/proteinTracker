import unittest, user, data_store

class test_create_user(unittest.TestCase):
    def test_weak_password(self):
        with self.assertRaises(ValueError):
            user.create_user("Bob", "bobZaBest@gmail.com", "password", 100)
    
    def test_new_user(self):
        user.create_user("Bob", "bobZaBest@gmail.com", "PaSSw0rd!", 100)
        user_info = data_store.get_data()["users"]
        self.assertTrue(len(user_info) == 1)
    
    def test_used_email(self):
        user.create_user("Bob", "bobZaBest@gmail.com", "PaSSw0rd!", 100)
        with self.assertRaises(ValueError):
            user.create_user("Not Bob",  "bobZaBest@gmail.com", "PaSSw0rd!", 70)

class Test_login(unittest.TestCase):
    def test_wrong_password(self):
        user.create_user("Bob", "bobZaBest@gmail.com", "PaSSw0rd!", 100)
        self.assertFalse(login("bobZaBest@gmail.com", "PaSSw0RD!"))

    def test_wrong_username(self):
        user.create_user("Bob", "bobZaBest@gmail.com", "PaSSw0rd!", 100)
        self.assertFalse(login("bobzaBest@gmail.com", "PaSSw0rd!"))
    
    def test_successful_login(self):
        user.create_user("Bob", "bobZaBest@gmail.com", "PaSSw0rd!", 100)
        self.assertTrue(login("bobZaBest@gmail.com", "PaSSw0rd!"))

if __name__ == '__main__':
    unittest.main()
