from django.test import TestCase
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from final_project.models import Course, Lecture, Administrator, TA, AccountType
from final_project.classes.administrator import Admin


class AllocateSectionsUnitTests(TestCase):
    def setUp(self):
        self.admin = Admin()
        self.systemAdmin = Administrator.objects.create(name="prof", email="adminTest@uwm.edu", password="123",
                                                        type=AccountType.Administrator,
                                                        phoneNumber=123456789, homeAddress="Milwaukee, WI")
        self.ta = TA.objects.create(name="ta", email="taTest@uwm.edu", password="123", type=AccountType.TA,
                                    phoneNumber=123456789, homeAddress="Milwaukee, WI")
        self.anotherTA = TA.objects.create(name="another ta", email="taAnotherTest@uwm.edu", password="456", type=AccountType.TA,
                                    phoneNumber=123456789, homeAddress="Milwaukee, WI")
        self.course = Course.objects.create(courseID=361, name='Introduction to Software Engineering', numLectures=1,
                                            numSections=3)
        self.unassignedCourse = Course.objects.create(courseID=110, name="Learn Coding", numLectures=1, numSections=1)
        self.lecture = Lecture.objects.create(lectureID=123, course=self.course)
        self.unassignedlLecture = Lecture.objects.create(lectureID=100, course=self.unassignedCourse)
        self.lecture.taID.add(self.ta)
        self.lecture.taID.add(self.anotherTA)

    def test_allocateSections_noTANoLec(self):
        with self.assertRaises(TypeError, msg="Admin allocating sections with invalid info did not raise TypeError"):
            a = self.admin.__allocateSections__('', '', 1)

    def test_allocateSections_noTA(self):
        with self.assertRaises(TypeError, msg="Admin allocating sections with no TA email did not raise TypeError"):
            a = self.admin.__allocateSections__('', '123', 1)

    def test_allocateSections_noLec(self):
        with self.assertRaises(TypeError, msg="Admin allocating sections with no lecture ID did not raise TypeError"):
            a = self.admin.__allocateSections__(self.ta.email, '', 1)

    def test_allocateSections_invalidTA(self):
        with self.assertRaises(ValueError, msg="Admin allocating sections with invalid TA email did not raise ValueError"):
            a = self.admin.__allocateSections__('notexistent@uwm.edu', '123', 1)

    def test_allocateSections_invalidLec(self):
        with self.assertRaises(ValueError, msg="Admin allocating sections with invalid lecture ID did not raise ValueError"):
            a = self.admin.__allocateSections__(self.ta.email, '000', 1)

    def test_allocateSections_invalidNumSections(self):
        with self.assertRaises(SyntaxError, msg="Admin allocating sections with invalid number of sections did not raise SyntaxError"):
            a = self.admin.__allocateSections__(self.ta.email, self.lecture.lectureID, 6)

    def test_allocateSections_validEntry_firstTA(self):
        self.assertTrue(self.admin.__allocateSections__(self.ta.email, self.lecture.lectureID, 2))

    def test_allocateSections_validEntry_secondTA(self):
        self.assertTrue(self.admin.__allocateSections__(self.anotherTA.email, self.lecture.lectureID, 3))

    def test_allocateSections_validEntry_noSec(self):
        self.assertTrue(self.admin.__allocateSections__(self.anotherTA.email, self.lecture.lectureID, 0))

    def test_allocateSections_validEntry_bothTAs(self):
        self.admin.__allocateSections__(self.ta.email, self.lecture.lectureID, 1)
        self.assertTrue(self.admin.__allocateSections__(self.anotherTA.email, self.lecture.lectureID, 2))

    def test_allocateSections_unassignedCourse(self):
        with self.assertRaises(ValueError, msg="Admin allocating sections with unassigned lecture did not raise ValueError"):
            a = self.admin.__allocateSections__(self.ta.email, self.unassignedlLecture.lectureID, 1)

    def test_allocateSections_invalidEntry_bothTAs(self):
        with self.assertRaises(SyntaxError, msg="Admin allocating sections with invalid number of sections did not raise SyntaxError"):
            self.admin.__allocateSections__(self.ta.email, self.lecture.lectureID, 3)
            a = self.admin.__allocateSections__(self.anotherTA.email, self.lecture.lectureID, 2)