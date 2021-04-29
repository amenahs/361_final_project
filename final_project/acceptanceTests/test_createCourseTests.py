from django.test import TestCase
from django.test import Client
from final_project.models import Course
from final_project.classes.administrator import Admin


class CreateCourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Admin()
        self.course = Course.objects.create(courseID=361, name='Introduction to Software Engineering')

    def test_createCourseExisting(self):
        resp = self.client.post('/create-course/', {'courseID': 361, 'name': 'Introduction to Software Engineering', 'lectureNum': 1, 'sectionNum': 3})
        self.assertEqual("Course already exists", resp.context["message"], msg="Creating non-unique course did not result in error message")

    def test_createCourseInvalidInput(self):
        resp = self.client.post('/create-course/', {'courseID': 395, 'name': '', 'lectureNum': 1, 'sectionNum': 0})
        self.assertEqual("Invalid input", resp.context["message"], msg="Creating course wtih invalid input did not result in error message")

    def test_createCourseNew_NoLecNoSec(self):
        resp = self.client.post('/create-course/', {'courseID': 315, 'name': 'Assembly Programming', 'lectureNum': 0, 'sectionNum': 0})
        self.assertEqual('/create-course/', resp.url, msg="Creating unique course with no lecture or sections was not successful")

    def test_createCourseNew_OneLecNoSec(self):
        resp = self.client.post('/create-course/', {'courseID': 395, 'name': 'Ethics in Computing', 'lectureNum': 1, 'sectionNum': 0})
        self.assertEqual('/create-course/', resp.url, msg="Creating unique course with one lecture and no sections was not successful")

    def test_createCourseNew_MultLecAndSec(self):
        resp = self.client.post('/create-course/', {'courseID': 337, 'name': 'Systems Programming', 'lectureNum': 2, 'sectionNum': 3})
        self.assertEqual('/create-course/', resp.url, msg="Creating unique course with multiple lectures and sections was not successful")

