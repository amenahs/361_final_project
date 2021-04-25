from final_project.classes.accounts import Accounts
from final_project.classes.assign import Assign
from final_project.models import User, Administrator, Professor, TA, Course


class Admin(Assign, Accounts):
    def __createAccount__(self, name, email, password, account, phoneNum, address):
        accountExists = False

        try:
            a = User.objects.get(email=email)
            accountExists = True
        except:
            newAcc = None
            if account=="A":
                newAcc = Administrator.objects.create(name=name, email=email, password=password, type=account, phoneNumber=phoneNum, address=address)
            elif account=="P":
                newAcc = Professor.objects.create(name=name, email=email, password=password, type=account, phoneNumber=phoneNum, address=address)
            elif account=="T":
                newAcc = TA.objects.create(name=name, email=email, password=password, type=account, phoneNumber=phoneNum, address=address)
            else:
                return TypeError("Invalid account type")

            newAcc.save()
            return newAcc

        if accountExists:
            raise ValueError("Account exists already")


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