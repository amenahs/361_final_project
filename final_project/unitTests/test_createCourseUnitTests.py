from django.test import TestCase
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from final_project.models import Course, Lecture, Section
from final_project.classes.administrator import Admin


class CreateCourseUnitTests(TestCase):
    def setUp(self):
        self.admin = Admin()
        self.course = Course.objects.create(courseID=337, name='Systems Programming')

    def test_createNewCourse_noLecNoSec(self):
        c = self.admin.__createCourse__(250, 'Introductory Programming', 0, 0)
        self.assertEqual(c, Course.objects.get(courseID=250), msg="New course was not created successfully")

    def test_createNewCourse_noLecNoSec_noLec(self):
        c = self.admin.__createCourse__(250, 'Introductory Programming', 0, 0)
        self.assertEqual(0, len(Lecture.objects.filter(course=c)), msg="Course was created with lecture(s)")

    def test_createNewCourse_noLecNoSec_noSec(self):
        c = self.admin.__createCourse__(250, 'Introductory Programming', 0, 0)
        self.assertEqual(0, len(Section.objects.filter(course=c)), msg="Course was created with section(s)")

    def test_createNewCourseWithLec(self):
        c = self.admin.__createCourse__(395, 'Ethics in Computing', 1, 0)
        self.assertEqual(c, Course.objects.get(courseID=395), msg="New course was not created successfully")

    def test_createNewCourseWithLec_oneLec(self):
        c = self.admin.__createCourse__(395, 'Ethics in Computing', 1, 0)
        self.assertEqual(1, len(Lecture.objects.filter(course=c)), msg="Lecture of new course was not created successfully")

    def test_createNewCourseWithLec_noSec(self):
        c = self.admin.__createCourse__(395, 'Ethics in Computing', 1, 0)
        self.assertEqual(0, len(Section.objects.filter(course=c)), msg="Course was created with section(s)")

    def test_createNewCourse_multLecAndSections(self):
        c = self.admin.__createCourse__(315, 'Assembly Language', 2, 3)
        self.assertEqual(c, Course.objects.get(courseID=315), msg="New course was not created successfully")

    def test_createNewCourse_multLecAndSections_multLec(self):
        c = self.admin.__createCourse__(315, 'Assembly Language', 2, 3)
        self.assertEqual(2, len(Lecture.objects.filter(course=c)), msg="2 Lectures of new course was not created successfully")

    def test_createNewCourse_multLecAndSections_multSec(self):
        c = self.admin.__createCourse__(315, 'Assembly Language', 2, 3)
        self.assertEqual(3, len(Section.objects.filter(course=c)), msg="3 Sections of new course was not created successfully")

    def test_createCourseInvalidInfo(self):
        with self.assertRaises(TypeError, msg="Admin creating a course with invalid info did not raise TypeError"):
            self.admin.__createCourse__("", "", 1, 0)

    def test_createCourseAlreadyExisting(self):
        with self.assertRaises(ValueError, msg="Admin creating a course that already exists did not raise ValueError"):
            self.admin.__createCourse__(337, 'Systems Programming', 1, 2)

