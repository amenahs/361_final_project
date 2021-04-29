from django.shortcuts import render, redirect
from django.views import View
from .models import User, Course, Lecture, Section
from .classes.administrator import Admin
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
            return render(request, "home.html", {"message":"user does not exist"})
        elif badPassword:
            return render(request, "home.html", {"message":"bad password"})
        else:
            request.session["email"] = m.email
            return redirect("/dashboard/")


class Dashboard(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")
        return render(request, "dashboard.html", {})


class CreateAccount(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        users = User.objects.all()
        formattedUsers = []
        for u in users:
            formattedUsers.append((u.email, u.name, u.type, u.phoneNumber, u.homeAddress))
        return render(request, "create-account.html", {"users": formattedUsers})

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
        return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                "accountPassword": u.password, "accountPhoneNumber": u.phoneNumber, "accountAddress": u.homeAddress})

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phoneNum = request.POST['number']
        address = request.POST['address']
        u = User.objects.get(email=request.session["email"])
        if not name or not email or not password or not address:
            return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                             "accountPassword": u.password,
                                                             "accountPhoneNumber": u.phoneNumber,
                                                             "accountAddress": u.homeAddress,
                                                             "message": "Invalid input"})
        u.name = name
        u.email = email
        u.password = password
        u.phoneNumber = phoneNum
        u.homeAddress = address
        u.save()
        return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                "accountPassword": u.password, "accountPhoneNumber": u.phoneNumber, "accountAddress": u.homeAddress, "message": "Information updated"})
