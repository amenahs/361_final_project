from final_project.models import Administrator, Course


class Admin():
    def __createCourse__(self, newCourseID, newCourseName):
        if not newCourseID or not newCourseName:
            raise TypeError("invalid input")

        courseExists = False

        try:
            c = Course.objects.get(courseID=newCourseID)
            courseExists = True
        except:
            newCourse = Course.objects.create(courseID=newCourseID, name=newCourseName)
            newCourse.save()
            return newCourse
        if courseExists:
            raise ValueError("course exists already")

    def __accessData__(self):
        pass