from django.test import TestCase
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from final_project.models import Course
from final_project.classes.administrator import Admin


class CreateCourseUnitTests(TestCase):
    def setUp(self):
        self.admin = Admin()
        self.course = Course.objects.create(courseID=337, name='Systems Programming')
        
    def test_createNewCourse(self):
        c = self.admin.__createCourse__(395, 'Ethics in Computing')
        self.assertEqual(c, Course.objects.get(courseID=395), msg="New course was not created successfully")

    def test_createCourseInvalidInfo(self):
        with self.assertRaises(TypeError, msg="Admin creating a course with invalid info did not raise TypeError"):
            self.admin.__createCourse__("", "")

    def test_createCourseAlreadyExisting(self):
        with self.assertRaises(ValueError, msg="Admin creating a course that already exists did not raise ValueError"):
            self.admin.__createCourse__(337, 'Systems Programming')

