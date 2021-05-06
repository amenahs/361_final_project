from django.test import TestCase
from django.test import Client
from final_project.models import Administrator, Professor, Lecture, Course

class addProfCourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prof = Professor.objects.create(name="prof",email="profTest@uwm.edu", password="123", type="P", phoneNumber=123456789, homeAddress="Milwaukee, WI")
        self.course = Course.objects.create(courseID='361', name='Introduction to Software Engineering')
        self.lecture = Lecture.objects.create(lectureID='123', course=self.course)

    def test_noProf(self):
        resp = self.client.post('/assign-prof-course/', {'prof': '', 'lecture': '123'})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No professor selected did not result in error message for professor assignment")

    def test_invalidProf(self):
        resp = self.client.post('/assign-prof-course/', {'prof': 'invalid@uwm.edu', 'lecture': '123'})
        self.assertEqual(resp.context["message"], "Professor or lecture does not exist", msg="Invalid professor selected did not result in error message for professor assignment")

    def test_noCourse(self):
        resp = self.client.post('/assign-prof-course/', {'prof': 'profTest@uwm.edu', 'lecture': ''})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No lecture selected did not result in error message for professor assignment")

    def test_invalidCourse(self):
        resp = self.client.post('/assign-prof-course/', {'prof': 'profTest@uwm.edu', 'lecture': '000'})
        self.assertEqual(resp.context["message"], "Professor or lecture does not exist",
                         msg="Invalid lecture selected did not result in error message for professor assignment")

    def test_validEntry(self):
        resp = self.client.post('/assign-prof-course/', {'prof': 'profTest@uwm.edu', 'lecture': '123'})
        self.assertEqual(resp.url, '/assign-prof-course/', msg='User was not redirected back to page after assigning course with valid input for proffessor')


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

