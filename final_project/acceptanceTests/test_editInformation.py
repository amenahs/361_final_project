from django.test import TestCase
from django.test import Client
from final_project.models import User, TA, AccountType


class EditInformationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(name="Name", email="username@uwm.edu", password="123", type=AccountType.Professor, phoneNumber=1234567890, homeAddress="Milwaukee, WI")
        self.ta = TA.objects.create(name="New TA", email="newta@uwm.edu", password="abc", type=AccountType.TA, phoneNumber=123456790, homeAddress="Milwaukee, WI")

    def test_invalidInput(self):
        response = self.client.post('/', {'email': 'username@uwm.edu', 'password': '123'})
        resp = self.client.post("/edit-information/", {'name': '', 'email': 'username@uwm.edu', 'password': '123', 'number': 1234567890, 'address': 'Milwaukee, WI'})
        self.assertEqual(resp.context["message"], "Invalid input", msg="Failed to give invalid input message with no name")

    def test_validInput(self):
        response = self.client.post('/', {'email': 'username@uwm.edu', 'password': '123'})
        resp = self.client.post("/edit-information/",
                                    {'name': 'New Name', 'email': 'username@uwm.edu', 'password': '123', 'number': 1234567890,
                                     'address': 'Milwaukee, WI'})
        self.assertEqual(resp.context["message"], "Information updated", msg="Failed to give information updated message with valid info")

    def test_noChange(self):
        response = self.client.post('/', {'email': 'username@uwm.edu', 'password': '123'})
        resp = self.client.post("/edit-information/",
                                {'name': 'Name', 'email': 'username@uwm.edu', 'password': '123',
                                 'number': 1234567890,
                                 'address': 'Milwaukee, WI'})
        self.assertEqual(resp.context["message"], "No changes made",
                         msg="Failed to give no changes made message with unchanged info")

    def test_taAddSkills(self):
        response = self.client.post('/', {'email': 'newta@uwm.edu', 'password': 'abc'})
        resp = self.client.post("/edit-information/",
                                {'name': 'New TA', 'email': 'ta@uwm.edu', 'password': 'abc',
                                 'number': 1234567890,
                                 'address': 'Milwaukee, WI',
                                 'skills': 'Java,CSS'})
        self.assertEqual(resp.context["message"], "Information updated",
                         msg="Failed to give information updated message with valid info and skills")


