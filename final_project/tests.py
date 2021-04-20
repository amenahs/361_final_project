from django.test import TestCase


class userLoginTestClass(unittest.TestCase):
    def setUp(self):
        # test to setup testers
        pass

    def testNoPassword(self):
        # test for when no password is provided
        pass

    def testOtherUserPassword(self):
        # test for if another user's password is used
        pass

    def testWrongPassword(self):
        # test a generally wrong password
        pass

    def testNoUser(self):
        # test if no user is inputted
        pass

    def testValidPassword(self):
        # test if a valid password is entered
        pass

class MyTestCase(unittest.TestCase):
    def setUp(self):

    def test_create_account(self):
        #test that account is created correctly with username and password

    def test_invalid_acc(self):
        #test that account is not created with incorrect username
        #and/or password

    def test_existing_acc(self):
        #test that new account is not created if username correlates to
        #a pre-existing account
        
