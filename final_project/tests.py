from django.test import TestCase
import unittest

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

class CreateCourseTests(unittest.TestCase):

    def setUpCourses(self):
        self.admin = Administrator("Admin", "admin@uwm.edu")
        self.prof = Professor("Prof", "prof@uwm.edu")
        self.course0 = Course()
        self.course1 = Course("CS 361", ["Lab 1", "Lab 2", "Lab 3"])

    def test_create_course(self):
        self.admin.createCourse(self.course1)
        self.assertEqual(self.admin.accessData().courses, self.course1, msg="New course was not created successfully")

    def test_create_course_invalid_information(self):
        with self.assertRaises(TypeError, msg="Admin creating a course with invalid input did not raise error"):
            self.admin.createCourse(self.course0)

    def test_create_course_already_existing(self):
        self.assertEqual(self.admin.createCourse(), "Course has already been created",
            msg="Incorrect error message when trying to create a course that already exists")

    def test_create_course_invalid_permissions(self):
        with self.assertRaises(PermissionError, msg="Non-admin creating a course did not raise error"):
            self.prof.createCourse(self.course1)