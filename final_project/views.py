from django.shortcuts import render, redirect
from django.views import View
from .models import User, Administrator, Professor, TA, Course, Lecture, Section, AccountType
from .classes.administrator import Admin
from .classes.user import UserAccount
# Create your views here.

class Home(View):
    def get(self, request):
        request.session.pop("email", None)
        return render(request, "home.html", {})
    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = User.objects.get(email=request.POST['email'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser:
            return render(request, "home.html", {"message": "User does not exist"})
        elif badPassword:
            return render(request, "home.html", {"message": "Bad password"})
        else:
            request.session["email"] = m.email
            return redirect("/dashboard/")


class Dashboard(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")
        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type==AccountType.Administrator
        return render(request, "dashboard.html", {'isAdmin': isAdmin})


class CreateAccount(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type==AccountType.Administrator
        if not isAdmin:
            return redirect("/dashboard/")

        admins = Administrator.objects.all()
        formattedAdmins = []
        for a in admins:
            formattedAdmins.append((a.email, a.name, a.phoneNumber, a.homeAddress))

        prof = Professor.objects.all()
        formattedProf = []
        for p in prof:
            formattedProf.append((p.email, p.name, p.phoneNumber, p.homeAddress))

        tas = TA.objects.all()
        formattedTA = []
        for t in tas:
            formattedTA.append((t.email, t.name, t.phoneNumber, t.homeAddress))

        return render(request, "create-account.html", {"admins": formattedAdmins, "prof": formattedProf,
                                                       "tas": formattedTA})

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        type = request.POST['type']
        phoneNum = request.POST['number']
        address = request.POST['address']

        try:
            a = Admin()
            a.__createAccount__(name, email, password, type, phoneNum, address)
        except ValueError:
            return render(request, "create-account.html", {"message": "Account already exists"})
        except TypeError:
            return render(request, "create-account.html", {"message": "Invalid input"})
        else:
            return redirect("/create-account/")


class CreateCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type==AccountType.Administrator
        if not isAdmin:
            return redirect("/dashboard/")

        courses = Course.objects.all()
        formattedCourses = []
        for c in courses:
            formattedCourses.append((c.courseID, c.name))
        lectures = Lecture.objects.all()
        formattedLectures = []
        for l in lectures:
            formattedLectures.append((l.course.courseID, l.lectureID))
        sections = Section.objects.all()
        formattedSections = []
        for s in sections:
            formattedSections.append((s.course.courseID, s.sectionID))

        return render(request, "create-course.html", {"courses": formattedCourses, "lectures": formattedLectures, "sections": formattedSections})

    def post(self, request):
        newCourseID = request.POST['courseID']
        newCourseName = request.POST['name']
        lectureNum = request.POST['lectureNum']
        sectionNum = request.POST['sectionNum']
        try:
            a = Admin()
            a.__createCourse__(newCourseID, newCourseName, lectureNum, sectionNum)
        except ValueError:
            return render(request, "create-course.html", {"message": "Course already exists"})
        except TypeError:
            return render(request, "create-course.html", {"message": "Invalid input"})
        else:
            return redirect("/create-course/")

class EditInformation(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")
        u = User.objects.get(email=request.session["email"])
        isTA = False

        if u.type == AccountType.TA:
            isTA = True
            ta = TA.objects.get(email=u.email)
            return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                             "accountPassword": u.password,
                                                             "accountPhoneNumber": u.phoneNumber,
                                                             "accountAddress": u.homeAddress,
                                                             "accountSkills": ta.skills,
                                                             "TA": isTA})

        return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                            "accountPassword": u.password,
                                                            "accountPhoneNumber": u.phoneNumber,
                                                            "accountAddress": u.homeAddress,
                                                            "TA": isTA})

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phoneNum = int(request.POST['number'])
        address = request.POST['address']
        u = User.objects.get(email=request.session["email"])

        isTA = False
        taSkills = ''
        if u.type == AccountType.TA:
            isTA = True
            taSkills = request.POST['skills']
        try:
            account = UserAccount()
            changesMade = account.__editContactInfo__(u.email, name, email, password, phoneNum, address, taSkills)
        except TypeError:
            return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                             "accountPassword": u.password,
                                                             "accountPhoneNumber": u.phoneNumber,
                                                             "accountAddress": u.homeAddress,
                                                             "message": "Invalid input",
                                                             "TA": isTA})
        except ValueError:
            return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                             "accountPassword": u.password,
                                                             "accountPhoneNumber": u.phoneNumber,
                                                             "accountAddress": u.homeAddress,
                                                             "message": "User does not exist",
                                                             "TA": isTA})
        message = 'No changes made'
        if changesMade:
            message = 'Information updated'
        u = User.objects.get(email=email)
        if isTA:
            ta = TA.objects.get(email=email)
            return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                             "accountPassword": u.password,
                                                             "accountPhoneNumber": u.phoneNumber,
                                                             "accountAddress": u.homeAddress,
                                                             "accountSkills": ta.skills,
                                                             "message": message,
                                                             "TA": isTA})

        return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                        "accountPassword": u.password,
                                                         "accountPhoneNumber": u.phoneNumber,
                                                         "accountAddress": u.homeAddress,
                                                         "message": message,
                                                         "TA": isTA})