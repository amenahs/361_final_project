from django.test import TestCase
from django.test import Client
from final_project.models import User

class addProfCourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Administrator("Admin", "admin@uwm.edu")
        self.inst = Professor.objects.create("Inst", "inst@uwm.edu")
        self.course = Course.objects.create(courseID='CS 361', name='Introduction to Software Engineering')

    def test_noProf(self):
        resp = self.client.post('/assigncourse-prof', {'instructor': '', 'course': 'CS 361'})
        self.assertEqual(resp.context["message"], "Must select an instructor.", msg="No professor selected did not result in error message for professor assignment")

    def test_noCourse(self):
        resp = self.client.post('/assigncourse-prof', {'instructor': 'inst@uwm.edu', 'course': ''})
        self.assertEqual(resp.context["message"], "Must select a course.", msg="No course selected did not result in error message for professor assignment")

    def test_validEntry(self):
        resp = self.client.post('/assigncourse-prof', {'instructor': 'inst@uwm.edu', 'course': 'CS 361'})
        self.assertEqual(resp.url, '/dashboard/', msg='User was not redirected to dashboard page after assigning course with valid input for proffessor')


class addTACourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = Administrator("Admin", "admin@uwm.edu")
        self.ta = TA.objects.create("TA", "ta@uwm.edu")
        self.course = Course.objects.create(courseID='CS 361', name='Introduction to Software Engineering')

    def test_noProf(self):
        resp = self.client.post('/assigncourse-ta', {'ta': '', 'course': 'CS 361'})
        self.assertEqual(resp.context["message"], "Must select a TA.", msg="No ta selected did not result in error message for ta assignment")

    def test_noCourse(self):
        resp = self.client.post('/assigncourse-ta', {'ta': 'ta@uwm.edu', 'course': ''})
        self.assertEqual(resp.context["message"], "Must select a course.", msg="No course selected did not result in error message for ta assignment")

    def test_validEntry(self):
        resp = self.client.post('/assigncourse-ta', {'ta': 'ta@uwm.edu', 'course': 'CS 361'})
        self.assertEqual(resp.url, '/dashboard/', msg='User was not redirected to dashboard page after assigning course to ta with valid input')

