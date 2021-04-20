from django.test import TestCase

# Create your tests here.
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

class AssignCourseTest(unittest.TestCase):
    def setUp(self):

    def test_assign_inst(self):
        #test that instructor is correctly assigned to course by admin

    def test_assign_ta(self):
        #test that ta is correctly assigned to course by admin

    def test_assign_admin(self):
        #test that administrator cannot be assigned to course

    def test_not_admin_inst(self):
        #test that course cannot be assigned by instructor

    def test_not_admin_ta(self):
        #test that course cannot be assigned by ta
