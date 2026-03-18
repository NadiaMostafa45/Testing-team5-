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
    
