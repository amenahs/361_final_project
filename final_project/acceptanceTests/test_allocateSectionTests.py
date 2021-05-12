from django.test import TestCase
from django.test import Client
from final_project.models import TA, Lecture, Course, AccountType


class AllocateSectionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.ta = TA.objects.create(name="New TA", email="testta@uwm.edu", password="abc", type=AccountType.TA, phoneNumber=123456790, homeAddress="Milwaukee, WI")
        self.course = Course.objects.create(courseID=361, name='Introduction to Software Engineering', numLectures=1, numSections=2)
        self.lecture = Lecture.objects.create(lectureID=123, course=self.course)
        self.lecture.taID.add(self.ta)

    def test_invalidSectionNum(self):
        resp = self.client.post('/allocate-sections/', {'taEmail': 'testta@uwm.edu', 'lecID': 123, 'sectionNum': 4})
        self.assertEqual(resp.context["message"], 'Invalid number of sections selected', msg="Invalid num of sections selected did not result in correct error message")

    def test_noTA(self):
        resp = self.client.post('/allocate-sections/', {'taEmail': '', 'lecID': 123, 'sectionNum': 2})
        self.assertEqual(resp.context["message"], 'Invalid input', msg="No TA did not result in correct error message")

    def test_invalidTA(self):
        resp = self.client.post('/allocate-sections/', {'taEmail': 'invalidta@uwm.edu', 'lecID': 123, 'sectionNum': 2})
        self.assertEqual(resp.context["message"], 'TA lecture assignment does not exist', msg="Invalid TA did not result in correct error message")

    def test_noLec(self):
        resp = self.client.post('/allocate-sections/', {'taEmail': 'testta@uwm.edu', 'lecID': '', 'sectionNum': 2})
        self.assertEqual(resp.context["message"], 'Invalid input', msg="No lecture did not result in correct error message")

    def test_invalidLec(self):
        resp = self.client.post('/allocate-sections/', {'taEmail': 'testta@uwm.edu', 'lecID': 000, 'sectionNum': 2})
        self.assertEqual(resp.context["message"], 'TA lecture assignment does not exist', msg="Invalid lec did not result in correct error message")

    def test_validEntry(self):
        resp = self.client.post('/allocate-sections/', {'taEmail': 'testta@uwm.edu', 'lecID': 123, 'sectionNum': 1})
        self.assertEqual(resp.url, '/assign-ta-course/', msg="Valid entry did not redirect to correct page")



