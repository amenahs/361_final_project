from django.test import TestCase
from django.test import Client
from final_project.models import User, Course
# TODO admin/prof/ta models, labs

class CreateCourseTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create(email='user@gmail.com', password='1234', phoneNumber=1234567890)
        self.course1 = Course.objects.create(courseID='CS 361', name='Introduction to Software Engineering')

    def test_create_course(self):
       # self.admin.createCourse(self.course1)
        self.assertEqual(Course.objects.get(courseID="CS 361"), self.course1, msg="New course was not created successfully")

    def test_create_course_invalid_information(self):
       #  with self.assertRaises(TypeError, msg="Admin creating a course with invalid input did not raise error"):
        #    self.admin.createCourse(Course.objects.create())
        pass

    def test_create_course_already_existing(self):
        self.assertEqual(Course.objects.create(courseID='CS 361', name='Introduction to Software Engineering'),
            "Course has already been created",
            msg="Incorrect error message when trying to create a course that already exists")

    def test_create_course_invalid_permissions(self):
      #  with self.assertRaises(PermissionError, msg="Non-admin creating a course did not raise error"):
         #   self.prof.createCourse(self.course1)
        pass