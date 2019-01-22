'''
For privacy reason, I only put sha256 of your name(lowercase).
'''
hashed_no_thanks_users = [
    'a95e24a50028a0aee37733984b0cfe64e9c93e81c21005e4e0bda2836d70eb08',  # 'no_thanks_username' for test
    '7e0e139183059fd276c2863d5ef3ced4c1605c4a9559f2d6895c18dd64d22125',
    '364e76541c21a3081a1fa0c315903992d8db3525cd77871b1e2b23dc5da88c2e',
    'df2f523d04bac3c19180243db46f305216a763c1a72e7e7fee9e27fbb6d14b98',
    '1a1a23b552ae021b5e51116f6c0ac06b5896385948a4e49c440166c7f6151214',
    '073f9d9ad7d5080d9eed1f2e643367ad1d0364f2fa2305b1413df3b72e54c994',
]

import hashlib


def hash_username(username):
    sha256 = hashlib.sha256()
    sha256.update(username.lower().encode())
    hashed_text = sha256.hexdigest()
    return hashed_text


def is_no_thanks_user(username):
    hashed_username = hash_username(username)
    return bool(hashed_username in hashed_no_thanks_users)


import unittest


class TestRejectUsers(unittest.TestCase):
    def test_is_no_thanks_user(self):
        self.assertTrue(is_no_thanks_user('no_thanks_username'))
        self.assertFalse(is_no_thanks_user('okay_username'))


if __name__ == '__main__':
    unittest.main(failfast=True)
