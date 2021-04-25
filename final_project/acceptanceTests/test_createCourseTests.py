from django.test import TestCase
from django.test import Client
from final_project.models import Administrator, Course
from final_project.classes.administrator import Admin


class CreateCourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Admin()
        self.course = Course.objects.create(courseID='CS 361', name='Introduction to Software Engineering')

    def test_createCourseExisting(self):
        resp = self.client.post('/create-course/', {'courseID': 'CS 361', 'name': 'Introduction to Software Engineering'})
        self.assertEqual("Course already exists", resp.context["message"], msg="Creating non-unique course did not result in error message")

    def test_createCourseInvalidInput(self):
        resp = self.client.post('/create-course/', {'courseID': '', 'name': ''})
        self.assertEqual("Invalid input", resp.context["message"], msg="Creating course wtih invalid input did not result in error message")

    def test_createCourseNew(self):
        resp = self.client.post('/create-course/', {'courseID': "CS 337", 'name': "Systems Programming"})
        self.assertEqual("Course successfully created", resp.context["message"], msg="Creating unique course was not successful")

# unit tests below

    def test_createNewCourse(self):
        c = self.admin.__createCourse__("CS 395", "Ethics in Computing")
        self.assertEqual(c, Course.objects.get(courseID="CS 395"), msg="New course was not created successfully")

    def test_createCourseInvalidInfo(self):
        with self.assertRaises(TypeError, msg="Admin creating a course with invalid info did not raise TypeError"):
            self.admin.__createCourse__("", "")

    def test_createCourseAlreadyExisting(self):
        with self.assertRaises(ValueError, msg="Admin creating a course that already exists did not raise ValueError"):
            self.admin.__createCourse__("CS 361", "Introduction to Software Engineering")

