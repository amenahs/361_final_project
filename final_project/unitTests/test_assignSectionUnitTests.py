from django.test import TestCase
from final_project.models import TA, Lecture, Course, Section, AccountType, TASectionAllocation
from final_project.classes.administrator import Admin


class AssignSectionUnitTests(TestCase):
    def setUp(self):
        self.admin = Admin()
        self.ta = TA.objects.create(name="New TA", email="testta@uwm.edu", password="abc", type=AccountType.TA, phoneNumber=123456790, homeAddress="Milwaukee, WI")
        self.course = Course.objects.create(courseID='361', name='Introduction to Software Engineering', numLectures=1, numSections=3)
        self.lecture = Lecture.objects.create(lectureID='123', course=self.course)
        self.lecture.taID.add(self.ta)
        self.section = Section.objects.create(sectionID='456', course=self.course)
        self.assignedSection = Section.objects.create(sectionID='987', course=self.course, taID=self.ta)
        self.taSectionAllocation = TASectionAllocation.objects.create(lec=self.lecture, ta=self.ta, numSections=2)

    def test_assignSec_noTANoSec(self):
        with self.assertRaises(TypeError, msg="Admin assigning section with invalid info did not raise TypeError"):
            a = self.admin.__assignTASection__('', '')

    def test_assignSec_noTA(self):
        with self.assertRaises(TypeError, msg="Admin assigning section with no TA did not raise TypeError"):
            a = self.admin.__assignTASection__('', self.section.sectionID)

    def test_assignSec_invalidTA(self):
        with self.assertRaises(ValueError, msg="Admin assigning section  with invalid TA did not raise ValueError"):
            a = self.admin.__assignTASection__('invalid@uwm.edu', self.section.sectionID)

    def test_assignSec_noSec(self):
        with self.assertRaises(TypeError, msg="Admin assigning section with no section did not raise TypeError"):
            a = self.admin.__assignTASection__(self.ta.email, '')

    def test_assignSec_invalidSec(self):
        with self.assertRaises(ValueError, msg="Admin assigning section  with invalid section did did not raise ValueError"):
            a = self.admin.__assignTASection__(self.ta.email, '000')

    def test_assignSec_alreadyAssigned(self):
        self.assertFalse(self.admin.__assignTASection__(self.ta.email, self.assignedSection.sectionID), msg="Admin assigning already assigned section did not return false")

    def test_assignSec_validEntry(self):
        self.assertTrue(self.admin.__assignTASection__(self.ta.email, self.section.sectionID), msg="Admin assigning valid section did not return true")

    def test_assignSec_maxAllocations(self):
        s = Section.objects.create(sectionID='678', course=self.course, taID=self.ta)
        with self.assertRaises(SyntaxError, msg="Admin assigning section with invalid section did did not raise SyntaxError"):
            a = self.admin.__assignTASection__(self.ta.email, self.assignedSection.sectionID)

