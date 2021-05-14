from django.test import TestCase
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from final_project.models import Course, Lecture, Administrator, Professor, TA, AccountType
from final_project.classes.administrator import Admin


class AssignCourseTest(TestCase):
        def setUp(self):
            self.admin = Admin()
            self.systemAdmin = Administrator.objects.create(name="prof", email="adminTest@uwm.edu", password="123", type=AccountType.Administrator,
                                                 phoneNumber=123456789, homeAddress="Milwaukee, WI")
            self.prof = Professor.objects.create(name="prof", email="profTest@uwm.edu", password="123", type=AccountType.Professor,
                                                 phoneNumber=123456789, homeAddress="Milwaukee, WI")
            self.ta = TA.objects.create(name="ta", email="taTest@uwm.edu", password="123", type=AccountType.TA,
                                                 phoneNumber=123456789, homeAddress="Milwaukee, WI")
            self.course = Course.objects.create(courseID='361', name='Introduction to Software Engineering', numLectures=1, numSections=0)
            self.lecture = Lecture.objects.create(lectureID='123', course=self.course)

        def test_assign_prof(self):
            # test that instructor is correctly assigned to course by admin
            self.assertTrue(self.admin.__assignProfessorLecture__(self.prof.email, self.lecture.lectureID), msg="Failed to assign professor to course correctly")

        def test_assign_ta(self):
            # test that ta is correctly assigned to course by admin
            self.assertTrue(self.admin.__assignTALecture__(self.ta.email, self.lecture.lectureID), msg="Failed to assign TA to course correctly")

        def test_assignprof_admin(self):
            # test that administrator cannot be assigned to course
            with self.assertRaises(ValueError, msg="Failed to raise error when assigning admin with assignProfessor"):
                self.admin.__assignProfessorLecture__(self.systemAdmin.email, self.lecture.lectureID)

        def test_assignta_admin(self):
            # test that administrator cannot be assigned to course
            with self.assertRaises(ValueError, msg="Failed to raise error when assigning admin with assignTACourse"):
                self.admin.__assignTALecture__(self.systemAdmin.email, self.lecture.lectureID)
