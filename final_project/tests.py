from django.test import TestCase
import unittest
from final_project.models import Administrator, Professor, Course


class userLoginTestClass(unittest.TestCase):
    def setUp(self):
        # test to setup testers
        pass

    def testNoPassword(self):
        # test for when no password is provided
        pass

    def testOtherUserPassword(self):
        # test for if another user's password is used
        pass

    def testWrongPassword(self):
        # test a generally wrong password
        pass

    def testNoUser(self):
        # test if no user is inputted
        pass

    def testValidPassword(self):
        # test if a valid password is entered
        pass

class CreateAccountTests(unittest.TestCase):
    def setUp(self):
        self.admin = Administrator("Admin", "admin@uwm.edu")
        self.account = Account("username@gmail.com", 12345)
        self.prof = Professor("Prof", "prof@uwm.edu")

    def test_create_account(self):
        #test that account is created correctly with username and password
        self.admin.createAccount(self.account)
        self.assertEqual(self.admin.accessData().account, self.account, msg="New account was not created successfully")

    def test_invalid_acc(self):
        #test that account is not created with incorrect username
        #and/or password
        with self.assertRaises(TypeError, msg="Admin creating an account with invalid input"):
            self.admin.createAccount(self.account)

    def test_existing_acc(self):
        #test that new account is not created if username correlates to
        #a pre-existing account
        self.assertEqual(self.admin.createAccount(), "Account has already been created",
                         msg="Incorrect error message when trying to create an account that already exists")

    def test_create_acc_invalid_permissions(self):
        #test that only admin/supervisor can create account
        with self.assertRaises(PermissionError, msg="Non-admin creating an account"):
            self.prof.createAccount(self.account)
        
class CreateCourseTests(unittest.TestCase):

    def setUp(self):
        self.admin = Administrator("Admin", "admin@uwm.edu")
        self.prof = Professor("Prof", "prof@uwm.edu")
        self.course0 = Course()
        self.course1 = Course("CS 361", ["Lab 1", "Lab 2", "Lab 3"])

    def test_create_course(self):
        self.admin.createCourse(self.course1)
        self.assertEqual(self.admin.accessData().courses, self.course1, msg="New course was not created successfully")

    def test_create_course_invalid_information(self):
        with self.assertRaises(TypeError, msg="Admin creating a course with invalid input did not raise error"):
            self.admin.createCourse(self.course0)

    def test_create_course_already_existing(self):
        self.assertEqual(self.admin.createCourse(), "Course has already been created",
            msg="Incorrect error message when trying to create a course that already exists")

    def test_create_course_invalid_permissions(self):
        with self.assertRaises(PermissionError, msg="Non-admin creating a course did not raise error"):
            self.prof.createCourse(self.course1)
            
class AssignCourseTest(unittest.TestCase):
    class AssignCourseTest(unittest.TestCase):
        def setUp(self):
            self.admin = Administrator("Admin", "admin@uwm.edu")
            self.inst = Professor("Inst", "inst@uwm.edu")
            self.ta = TA("TA", "ta@uwm.edu")
            self.course = Course("CS 361", [])

        def test_assign_inst(self):
            # test that instructor is correctly assigned to course by admin
            self.admin.assignProfessor(self.inst, self.course)
            self.assertEquals(self.inst.userID, self.course.professorID, msg="Failed to assign professor to course correctly")

        def test_assign_ta(self):
            # test that ta is correctly assigned to course by admin
            self.admin.assignTACourse(self.ta, self.course)
            self.assertTrue(self.ta.userID in self.course.taID, msg="Failed to assign TA to course correctly")

        def test_assignprof_admin(self):
            # test that administrator cannot be assigned to course
            with assertRaises(NameError, msg="Failed to raise error when assigning admin with assignProfessor"):
                self.admin.assignProfesor(self.admin)

        def test_assignta_admin(self):
            # test that administrator cannot be assigned to course
            with assertRaises(NameError, msg="Failed to raise error when assigning admin with assignTACourse"):
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
