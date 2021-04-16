import unittest

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.admin = Administrator("Admin", "admin@uwm.edu")
        self.prof = Professor("Prof", "prof@uwm.edu")
        self.course0 = Course()
        self.course1 = Course("CS 361", ["Lab 1", "Lab 2", "Lab 3"])

    def test_create_course(self):
        self.admin.createCourse(self.course1)
        self.assertEqual(Course.getCourses(), self.course1, msg="New course was not created successfully")

    def test_create_course_invalid_information(self):
        with self.assertRaises(TypeError, msg="Admin creating a course with invalid info did not raise error"):
            self.admin.createCourse(self.course0)

    def test_create_course_already_existing(self):
        self.assertEqual(self.admin.createCourse(), "Course has already been created", msg="Incorrect error message"
                                                            "when trying to create a course that already exists")

    def test_create_course_invalid_permissions(self):
        with self.assertRaises(PermissionError, msg="Non-admin creating a course did not raise error"):
            self.prof.createCourse(self.course1)



if __name__ == '__main__':
    unittest.main()
