import unittest

class User:
    def __init__(self, name, email): 
        self._name = name
        self._email = email

    def name(self, new_name=None):
        if new_name is not None:
            self._name = new_name
        return self._name

    def email(self, new_email=None):
        if new_email is not None:
            self._email = new_email
        return self._email

class TestUser(unittest.TestCase):
    
    def setUp(self):
        self.user = User("John Doe", "john.doe@example.com")

    def test_init(self):
        self.assertEqual(self.user.name(), "John Doe")
        self.assertEqual(self.user.email(), "john.doe@example.com")

    def test_update_name(self): 
        self.user.name("Nadia")
        self.assertEqual(self.user.name(), "Nadia")

    def test_update_email(self):
        self.user.email("nadia.doe@example.com")
        self.assertEqual(self.user.email(), "nadia.doe@example.com")

if __name__ == '__main__':
    unittest.main()