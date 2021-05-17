from django.test import TestCase
from django.test import Client
from final_project.models import Professor, TA, Lecture, Course, AccountType


class AssignProfCourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prof = Professor.objects.create(name="prof",email="profTest@uwm.edu", password="123", type=AccountType.Professor, phoneNumber=123456789, homeAddress="Milwaukee, WI")
        self.course = Course.objects.create(courseID=361, name='Introduction to Software Engineering', numLectures=1, numSections=0)
        self.lecture = Lecture.objects.create(lectureID=123, course=self.course)

    def test_noProf(self):
        resp = self.client.post('/assign-prof-course/', {'prof': '', 'lecture': '123'})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No professor selected did not result in error message for professor assignment")

    def test_invalidProf(self):
        resp = self.client.post('/assign-prof-course/', {'prof': 'invalid@uwm.edu', 'lecture': '123'})
        self.assertEqual(resp.context["message"], "Please select valid professor and lecture", msg="Invalid professor selected did not result in error message for professor assignment")

    def test_noLec(self):
        resp = self.client.post('/assign-prof-course/', {'prof': 'profTest@uwm.edu', 'lecture': ''})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No lecture selected did not result in error message for professor assignment")

    def test_invalidLec(self):
        resp = self.client.post('/assign-prof-course/', {'prof': 'profTest@uwm.edu', 'lecture': '000'})
        self.assertEqual(resp.context["message"], "Please select valid professor and lecture",
                         msg="Invalid lecture selected did not result in error message for professor assignment")

    def test_validEntry(self):
        resp = self.client.post('/assign-prof-course/', {'prof': 'profTest@uwm.edu', 'lecture': '123'})
        self.assertEqual(resp.url, '/assign-prof-course/', msg='User was not redirected back to page after assigning course with valid input for proffessor')


class AssignTACourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.ta = TA.objects.create(name="New TA", email="testta@uwm.edu", password="abc", type=AccountType.TA, phoneNumber=123456790, homeAddress="Milwaukee, WI")
        self.course = Course.objects.create(courseID=361, name='Introduction to Software Engineering', numLectures=1, numSections=0)
        self.lecture = Lecture.objects.create(lectureID=123, course=self.course)

    def test_noTA(self):
        resp = self.client.post('/assign-ta-course/', {'ta': '', 'lecture': '123'})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No ta selected did not result in error message for ta assignment")

    def test_invalidTA(self):
        resp = self.client.post('/assign-ta-course/', {'ta': 'invalid@uwm.edu', 'lecture': '123'})
        self.assertEqual(resp.context["message"], "Please select valid TA and lecture", msg="Invalid TA selected did not result in error message for professor assignment")

    def test_noLec(self):
        resp = self.client.post('/assign-ta-course/', {'ta': 'testta@uwm.edu', 'lecture': ''})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No lecture selected did not result in error message for ta assignment")

    def test_invalidLec(self):
        resp = self.client.post('/assign-ta-course/', {'ta': 'testta@uwm.edu', 'lecture': '000'})
        self.assertEqual(resp.context["message"], "Please select valid TA and lecture", msg="Invalid lecture selected did not result in error message for ta assignment")

