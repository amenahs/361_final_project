from final_project.classes.accounts import Accounts
from final_project.classes.assign import Assign
from final_project.models import User, Administrator, Professor, TA, Course, AccountType


class Admin(Assign, Accounts):
    def __createAccount__(self, name, email, password, account, phoneNum, address):
        accountExists = False

        try:
            a = User.objects.get(email=email)
            accountExists = True
        except:
            newAcc = None
            if account=='A':
                newAcc = Administrator.objects.create(name=name, email=email, password=password, type=AccountType.Administrator, phoneNumber=phoneNum, homeAddress=address)
            elif account=='P':
                newAcc = Professor.objects.create(name=name, email=email, password=password, type=AccountType.Professor, phoneNumber=phoneNum, homeAddress=address)
            elif account=='T':
                newAcc = TA.objects.create(name=name, email=email, password=password, type=AccountType.TA, phoneNumber=phoneNum, homeAddress=address)
            else:
                raise TypeError("Invalid input")

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