from django.test import TestCase
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from final_project.models import User, TA, AccountType
from final_project.classes.user import UserAccount


class EditInformationUnitTests(TestCase):
    def setUp(self):
        self.account = UserAccount()
        self.user = User.objects.create(name="name", email="username@uwm.edu", password="123", type=AccountType.Professor, phoneNumber=123456790, homeAddress="Milwaukee, WI")
        self.ta = TA.objects.create(name="New TA", email="newta@uwm.edu", password="abc", type=AccountType.TA, phoneNumber=123456790, homeAddress="Milwaukee, WI")
        self.newName = "New Name"
        self.taSkills = 'HTML,Java'

    def test_invalidData(self):
        with self.assertRaises(TypeError, msg="User editing info with invalid data did not raise TypeError"):
            self.account.__editContactInfo__('username@uwm.edu', '', '', '', 1234567890, 'Milwaukee, WI', '')

    def test_invalidUser(self):
        with self.assertRaises(ValueError, msg="Non-existent user did not raise ValueError"):
            self.account.__editContactInfo__('idonotexist@uwm.edu', 'user', 'username@uwm.edu', 'password', 1234567890, 'Milwaukee, WI', '')

    def test_validData_noChanges(self):
        c = self.account.__editContactInfo__('username@uwm.edu', 'name', 'username@uwm.edu', '123', 123456790, 'Milwaukee, WI', '')
        self.assertFalse(c, msg="No changes made still resulted in data being re-saved")

    def test_validData_changeName(self):
        self.account.__editContactInfo__('username@uwm.edu', self.newName, 'username@uwm.edu', '123', 1234567890, 'Milwaukee, WI', '')
        self.assertEqual(self.newName, User.objects.get(email='username@uwm.edu').name, msg="User editing info with valid data was not successful")

    def test_taAddSkills(self):
        self.account.__editContactInfo__('newta@uwm.edu', "TA", 'newta@uwm.edu', 'abcd', 1234567890, 'Milwaukee, WI', self.taSkills)
        self.assertEqual(self.taSkills, TA.objects.get(email='newta@uwm.edu').skills, msg="TA adding skills with valid data was not successful")

