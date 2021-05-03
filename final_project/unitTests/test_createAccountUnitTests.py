from django.test import TestCase
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from final_project.models import Professor, User
from final_project.classes.administrator import Admin


class CreateAccountUnitTests(TestCase):
    def setUp(self):
        self.admin = Admin()
        self.account = User.objects.create(name="name",email="username@uwm.edu", password="123", type="P", phoneNumber=123456790, homeAddress="Milwaukee, WI")
        self.prof = Professor("Prof", "prof@uwm.edu")

    def test_create_account(self):
        #test that account is created correctly with username and password
        r = self.admin.__createAccount__("prof", "prof@uwm.edu", "123", "P", 1234567, "Milwaukee, WI")
        self.assertEqual(r, Professor.objects.get(email="prof@uwm.edu"), msg="New account was not created successfully")

    def test_invalid_acc(self):
        #test that account is not created with incorrect username
        #and/or password
        with self.assertRaises(TypeError, msg="Admin creating an account with invalid input"):
            self.admin.__createAccount__("", "", "", "", 1, "")

    def test_existing_acc(self):
        #test that new account is not created if username correlates to
        #a pre-existing account
        with self.assertRaises(ValueError, msg="Account already existing"):
            self.admin.__createAccount__("name", "username@uwm.edu", "123", "P", 1234567, "Milwaukee, WI")
