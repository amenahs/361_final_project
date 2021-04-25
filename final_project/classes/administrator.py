from final_project.classes.accounts import Accounts
from final_project.classes.assign import Assign
from final_project.models import User, Administrator, Course


class Admin(Assign, Accounts):
    def __createCourse__(self, newCourseID, newCourseName):
        if not newCourseID or not newCourseName:
            raise TypeError("Invalid input")

        courseExists = False

        try:
            c = Course.objects.get(courseID=newCourseID)
            courseExists = True
        except:
            newCourse = Course.objects.create(courseID=newCourseID, name=newCourseName)
            newCourse.save()
            return newCourse
        if courseExists:
            raise ValueError("Course exists already")

    def __accessData__(self):
        pass