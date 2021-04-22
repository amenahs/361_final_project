from django.test import TestCase
import unittest


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

    def test_create_account(self):
        #test that account is created correctly with username and password

    def test_invalid_acc(self):
        #test that account is not created with incorrect username
        #and/or password

    def test_existing_acc(self):
        #test that new account is not created if username correlates to
        #a pre-existing account
        
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
            self.assertEquals(self.inst.userID, self.course.professorID, msg="Failed to assign professor correctly")

        def test_assign_ta(self):
            # test that ta is correctly assigned to course by admin
            self.admin.assignTACourse(self.ta, self.course)
            ###self.assertEquals(self.inst.userID, self.course., msg="Failed to assign TA correctly")

        def test_assign_admin(self):
            # test that administrator cannot be assigned to course
            with assertRaises

        def test_inst_assign_inst(self):
            # test that course cannot be assigned by instructor
            with assertRaises(PermissionError, msg="Instructor assigning instructor failed to raise error"):
                self.inst.assignProfessor(self.inst, self.course)

        def test_inst_assign_ta(self):
            # test that course cannot be assigned by ta
            with assertRaises(PermissionError, msg="Instructor assigning ta failed to raise error"):
                self.inst.assignTACourse(self.ta, self.course)

        def test_ta_assign_inst(self):
            # test that course cannot be assigned by instructor
            with assertRaises(PermissionError, msg="TA assigning instructor failed to raise error"):
                self.ta.assignProfessor(self.inst, self.course)

        def test_ta_assign_ta(self):
            # test that course cannot be assigned by ta
            with assertRaises(PermissionError, msg="TA assigning ta failed to raise error"):
                self.ta.assignTACourse(self.ta, self.course)
