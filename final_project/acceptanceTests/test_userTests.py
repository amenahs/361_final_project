from django.test import TestCase
from django.test import Client
from final_project.models import User


class UserLoginTestClass(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(email='user@gmail.com', password='1234', phoneNumber=1234567890)
        self.user2 = User.objects.create(email='anotheruser@gmail.com', password='5678', phoneNumber=1234567890)

    def test_noPassword(self):
        resp = self.client.post('/', {'email': 'user@gmail.com', 'password': ''})
        self.assertEqual(resp.context["message"], "bad password", msg="No password entered did not result in error message")

    def test_otherUserPassword(self):
        resp = self.client.post("/", {'email': 'user@gmail.com', 'password': '5678'})
        self.assertEqual(resp.context["message"], "bad password", msg="Another user's password entered did not result in error message")

    def test_wrongPassword(self):
        resp = self.client.post("/", {'email': 'user@gmail.com', 'password': 'hello'})
        self.assertEqual(resp.context["message"], "bad password", msg="Incorrect password entered did not result in error message")

    def test_noUser(self):
        resp = self.client.post("/", {'email': 'myemail@gmail.com', 'password': '5678'})
        self.assertEqual(resp.context["message"], "user does not exist", msg="Invalid username entered did not result in error message")

    def test_validPassword(self):
        resp = self.client.post('/', {'email': 'user@gmail.com', 'password': '1234'})
        self.assertEqual(resp.url, '/dashboard/', msg='User was not redirected to dashboard page after logging in with correct credentials')

