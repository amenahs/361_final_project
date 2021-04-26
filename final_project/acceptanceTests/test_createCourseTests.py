from django.test import TestCase
from django.test import Client
from final_project.models import Administrator, Course
from final_project.classes.administrator import Admin


class CreateCourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Admin()
        self.course = Course.objects.create(courseID=361, name='Introduction to Software Engineering')

    def test_createCourseExisting(self):
        resp = self.client.post('/create-course/', {'courseID':361, 'name': 'Introduction to Software Engineering'})
        self.assertEqual("Course already exists", resp.context["message"], msg="Creating non-unique course did not result in error message")

    def test_createCourseInvalidInput(self):
        resp = self.client.post('/create-course/', {'courseID':395, 'name': ''})
        self.assertEqual("Invalid input", resp.context["message"], msg="Creating course wtih invalid input did not result in error message")

    def test_createCourseNew(self):
        resp = self.client.post('/create-course/', {'courseID':337, 'name': "Systems Programming"})
        self.assertEqual("Course successfully created", resp.context["message"], msg="Creating unique course was not successful")

