from django.test import TestCase
from django.test import Client
from final_project.models import User


class CreateAccountTestClass(TestCase):
    def setUp(self):
        self.client = Client()
        self.account = User.objects.create(name="name", email="username@uwm.edu", password="123", type="P", phoneNumber=1234567, homeAddress="Milwaukee, WI")

    def testNoUserName(self):
        resp = self.client.post("/create-account/", {'name': 'user', 'email': '', 'password': '1234', 'number': 1234567, 'address': 'Milwaukee,WI', 'type': 'P'})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No username entered did not result in errror message")

    def testValidUsername(self):
        resp = self.client.post('/create-account/', {'name': 'user', 'email': 'user@gmail.com', 'password': '1234', 'number': 1234567, 'address': 'Milwaukee,WI', 'type': 'P'})
        self.assertEqual(resp.url, "/create-account/", msg="Valid username")

    def testOtherUserName(self):
        #if account already exists
        resp = self.client.post("/create-account/", {'name': 'name', 'email': 'username@uwm.edu', 'password': '123', 'number': 1234567, 'address': 'Milwaukee, WI', 'type': 'P'})
        self.assertEqual(resp.context["message"], "Account already exists", msg="Another user's email entered did not result in error message")

    def testNoPassword(self):
        resp = self.client.post('/create-account/', {'name': 'user', 'email': 'user@gmail.com', 'password': '', 'number': 1234567, 'address': 'Milwaukee,WI', 'type': 'P'})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No password entered did not result in error message")

    def testValidPassword(self):
        resp = self.client.post('/create-account/', {'name': 'user', 'email': 'user@gmail.com', 'password': '1234', 'number': 1234567, 'address': 'Milwaukee,WI', 'type': 'P'})
        self.assertEqual(resp.url, "/create-account/", msg="Valid password")

"""
    def test_create_acc_invalid_permissions(self):
        #test that only admin/supervisor can create account
        with self.assertRaises(PermissionError, msg="Non-admin creating an account"):
            self.prof.createAccount(self.account)
            """