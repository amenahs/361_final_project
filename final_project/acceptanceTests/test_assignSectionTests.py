from django.test import TestCase
from django.test import Client
from final_project.models import TA, Lecture, Course, Section, AccountType, TASectionAllocation


class AssignTASectionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.ta = TA.objects.create(name="New TA", email="testta@uwm.edu", password="abc", type=AccountType.TA, phoneNumber=123456790, homeAddress="Milwaukee, WI")
        self.course = Course.objects.create(courseID=361, name='Introduction to Software Engineering', numLectures=1, numSections=3)
        self.lecture = Lecture.objects.create(lectureID=123, course=self.course)
        self.lecture.taID.add(self.ta)
        self.section = Section.objects.create(sectionID=456, course=self.course)
        self.unassignedCourse = Course.objects.create(courseID=110, name="Learn Coding", numLectures=1, numSections=1)
        self.unassignedLec = Lecture.objects.create(lectureID=121, course=self.unassignedCourse)
        self.unassignedSec = Section.objects.create(sectionID=111, course=self.unassignedCourse)
        self.assignedSection = Section.objects.create(sectionID=987, course=self.course, taID=self.ta)
        self.taSectionAllocation = TASectionAllocation.objects.create(lec=self.lecture, ta=self.ta, numSections=2)

    def test_noTA(self):
        resp = self.client.post('/assign-ta-section/', {'ta': '', 'section': self.section.sectionID})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No ta selected did not result in error message for ta assignment")

    def test_invalidTA(self):
        resp = self.client.post('/assign-ta-section/', {'ta': 'invalid@uwm.edu', 'section': self.section.sectionID})
        self.assertEqual(resp.context["message"], 'Please select valid TA and section', msg="Invalid TA selected did not result in error message for professor assignment")

    def test_noSec(self):
        resp = self.client.post('/assign-ta-section/', {'ta': self.ta.email, 'section': ''})
        self.assertEqual(resp.context["message"], "Invalid input", msg="No section selected did not result in error message for ta assignment")

    def test_invalidSec(self):
        resp = self.client.post('/assign-ta-section/', {'ta': self.ta.email, 'section': '000'})
        self.assertEqual(resp.context["message"], 'Please select valid TA and section', msg="Invalid section selected did not result in error message for ta assignment")

    def test_alreadyAssigned(self):
        resp = self.client.post('/assign-ta-section/', {'ta': self.ta.email, 'section': self.assignedSection.sectionID})
        self.assertEqual(resp.context["message"], "Assignment already exists", msg="Invalid section selected did not result in error message for ta assignment")

    def test_notAssignedLec(self):
        resp = self.client.post('/assign-ta-section/', {'ta': self.ta.email, 'section': self.unassignedSec.sectionID})
        self.assertEqual(resp.context["message"],
                         "TA has not been assigned to that course, or has already been assigned "
                         "the maximum number of allocated sections",
                         msg="Unassigned lecture/section selected did not result in error message for ta assignment")

    def test_validEntry(self):
        resp = self.client.post('/assign-ta-section/', {'ta': self.ta.email, 'section': self.section.sectionID})
        self.assertEqual(resp.url, "/assign-ta-section/", msg='User was not redirected to correct page after assigning section to ta with valid input')


