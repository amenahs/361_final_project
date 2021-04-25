from django.test import TestCase
from django.test import Client
from final_project.models import User

class CreateAccountTestClass(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(email='user@gmail.com', password='1234', phoneNumber=1234567890)
        self.user2 = User.objects.create(email='anotheruser@gmail.com', password='5678', phoneNumber=1234567890)

    def testNoUserName(self):
        resp = self.client.post("/", {'email': '', 'password': '5678'})
        self.assertEqual(resp.context["message"], "user did not enter username", msg="Invalid username entered did not result in error message")

    def testValidUsername(self):
        resp = self.client.post('/', {'email': 'user@gmail.com', 'password': '1234'})
        self.assertEqual(resp.url, '/dashboard/', msg='Username accepted')

    def testOtherUserName(self):
        resp = self.client.post("/", {'email': 'user@gmail.com', 'password': '5678'})
        self.assertEqual(resp.context["message"], "bad password", msg="Another user's email entered did not result in error message")

    def testNoPassword(self):
        resp = self.client.post('/', {'email': 'user@gmail.com', 'password': ''})
        self.assertEqual(resp.context["message"], "bad password", msg="No password entered did not result in error message")

    def testValidPassword(self):
        resp = self.client.post('/', {'email': 'user@gmail.com', 'password': '1234'})
        self.assertEqual(resp.url, '/dashboard/', msg='User account created')
