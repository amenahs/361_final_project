import unittest
from final_project.models import Administrator, Professor
from final_project.classes.administrator import Admin


class CreateAccountUnitTests(unittest.TestCase):
    def setUp(self):
        self.admin = Administrator("Admin", "admin@uwm.edu")
        self.account = Account("username@gmail.com", 12345)
        self.prof = Professor("Prof", "prof@uwm.edu")

    def test_create_account(self):
        #test that account is created correctly with username and password
        self.admin.createAccount(self.account)
        self.assertEqual(self.admin.accessData().account, self.account, msg="New account was not created successfully")

    def test_invalid_acc(self):
        #test that account is not created with incorrect username
        #and/or password
        with self.assertRaises(TypeError, msg="Admin creating an account with invalid input"):
            self.admin.createAccount(self.account)

    def test_existing_acc(self):
        #test that new account is not created if username correlates to
        #a pre-existing account
        self.assertEqual(self.admin.createAccount(), "Account has already been created",
                         msg="Incorrect error message when trying to create an account that already exists")

    def test_create_acc_invalid_permissions(self):
        #test that only admin/supervisor can create account
        with self.assertRaises(PermissionError, msg="Non-admin creating an account"):
            self.prof.createAccount(self.account)



