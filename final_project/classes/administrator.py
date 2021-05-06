from final_project.classes.accounts import Accounts
from final_project.classes.assign import Assign
from final_project.models import User, Administrator, Professor, TA, Course, Lecture, Section, AccountType
from random import randint


class Admin(Assign, Accounts):
    def __createAccount__(self, name, email, password, account, phoneNum, address):
        if not name or not email or not password or not account or not address:
            raise TypeError("Invalid input")
        accountExists = False

        try:
            a = User.objects.get(email=email)
            accountExists = True
        except:
            newAcc = None
            if account==AccountType.Administrator:
                newAcc = Administrator.objects.create(name=name, email=email, password=password, type=AccountType.Administrator, phoneNumber=phoneNum, homeAddress=address)
            elif account==AccountType.Professor:
                newAcc = Professor.objects.create(name=name, email=email, password=password, type=AccountType.Professor, phoneNumber=phoneNum, homeAddress=address)
            elif account==AccountType.TA:
                newAcc = TA.objects.create(name=name, email=email, password=password, type=AccountType.TA, phoneNumber=phoneNum, homeAddress=address)
            else:
                raise TypeError("Invalid input")

            newAcc.save()
            return newAcc

        if accountExists:
            raise ValueError("Account exists already")

    def __createCourse__(self, newCourseID, newCourseName, lectureNum, sectionNum):
        if not newCourseID or not newCourseName:
            raise TypeError("Invalid input")

        courseExists = False

        try:
            c = Course.objects.get(courseID=newCourseID)
            courseExists = True
        except:
            newCourse = Course.objects.create(courseID=newCourseID, name=newCourseName, numLectures=lectureNum, numSections=sectionNum)
            newCourse.save()

            for i in range(0, int(lectureNum)):
                lecID = randint(100, 999)
                lec = Lecture.objects.create(course=newCourse, lectureID=lecID)
                lec.save()

            for j in range(0, int(sectionNum)):
                secID = randint(100, 999)
                sec = Section.objects.create(course=newCourse, sectionID=secID)
                sec.save()

            return newCourse
        if courseExists:
            raise ValueError("Course exists already")

    def __assignProfessorLecture__(self, profEmail, lecID):
        if not profEmail or not lecID:
            raise TypeError("Invalid input")
        try:
            lec = Lecture.objects.get(lectureID=lecID)
            prof = Professor.objects.get(email=profEmail)

            if lec.profID != prof:
                lec.profID = prof
                lec.save()
                return True

            return False

        except:
            raise ValueError("Professor or lecture does not exist")

    def __assignTALecture__(self, taEmail, lecID):
        if not taEmail or not lecID:
            raise TypeError("Invalid input")
        try:
            lec = Lecture.objects.get(lectureID=lecID)
            ta = TA.objects.get(email=taEmail)

            if lec.taID != ta:
                lec.taID = ta
                lec.save()
                return True

            return False

        except:
            raise ValueError("TA or lecture does not exist")

    def __assignTASection__(self, taEmail, secID):
        pass