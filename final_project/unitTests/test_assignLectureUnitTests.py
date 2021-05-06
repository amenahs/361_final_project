from django.test import TestCase
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from final_project.models import Course, Lecture, Professor, TA
from final_project.classes.administrator import Admin

class AssignCourseTest(TestCase):
        def setUp(self):
            self.admin = Admin()
            self.prof = Professor.objects.create(name="prof", email="profTest@uwm.edu", password="123", type="P",
                                                 phoneNumber=123456789, homeAddress="Milwaukee, WI")
            self.course = Course.objects.create(courseID='361', name='Introduction to Software Engineering')
            self.lecture = Lecture.objects.create(lectureID='123', course=self.course)

        def test_assign_inst(self):
            # test that instructor is correctly assigned to course by admin
            self.assertTrue(self.admin.__assignProfessorLecture__(self.prof.email, self.lecture.lectureID))
            #self.assertEquals(self.prof, self.lecture.profID, msg="Failed to assign professor to course correctly")

        def test_assign_ta(self):
            # test that ta is correctly assigned to course by admin
            self.admin.assignTACourse(self.ta, self.course)
            self.assertTrue(self.ta.userID in self.course.taID, msg="Failed to assign TA to course correctly")

        def test_assignprof_admin(self):
            # test that administrator cannot be assigned to course
            with self.assertRaises(NameError, msg="Failed to raise error when assigning admin with assignProfessor"):
                self.admin.assignProfesor(self.admin)

        def test_assignta_admin(self):
            # test that administrator cannot be assigned to course
            with self.assertRaises(NameError, msg="Failed to raise error when assigning admin with assignTACourse"):
                self.admin.assignTACourse(self.admin)

        def test_inst_assign_inst(self):
            # test that course cannot be assigned by instructor
            with self.assertRaises(PermissionError, msg="Instructor assigning instructor to coursefailed to raise error"):
                self.inst.assignProfessor(self.inst, self.course)

        def test_inst_assign_ta(self):
            # test that course cannot be assigned by ta
            with self.assertRaises(PermissionError, msg="Instructor assigning ta to course failed to raise error"):
                self.inst.assignTACourse(self.ta, self.course)

        def test_ta_assign_inst(self):
            # test that course cannot be assigned by instructor
            with self.assertRaises(PermissionError, msg="TA assigning instructor to course failed to raise error"):
                self.ta.assignProfessor(self.inst, self.course)

        def test_ta_assign_ta(self):
            # test that course cannot be assigned by ta
            with self.assertRaises(PermissionError, msg="TA assigning ta to course failed to raise error"):
                self.ta.assignTACourse(self.ta, self.course)
