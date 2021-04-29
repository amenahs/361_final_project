from django.shortcuts import render, redirect
from django.views import View
from .models import User, Course
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

        users = User.objects.filter()
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
            users = User.objects.filter()
            formattedUsers = []
            for u in users:
                formattedUsers.append((u.email, u.name, u.type, u.phoneNumber, u.homeAddress))
            return render(request, "create-account.html", {"message": "Account successfully created", "users": formattedUsers})


class CreateCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        courses = Course.objects.filter()
        formattedCourses = []
        for c in courses:
            formattedCourses.append((c.courseID, c.name))
        return render(request, "create-course.html", {"courses": formattedCourses})

    def post(self, request):
        newCourseID = request.POST['courseID']
        newCourseName = request.POST['name']
        try:
            a = Admin()
            a.__createCourse__(newCourseID, newCourseName)
        except ValueError:
            return render(request, "create-course.html", {"message": "Course already exists"})
        except TypeError:
            return render(request, "create-course.html", {"message": "Invalid input"})
        else:
            courses = Course.objects.filter()
            formattedCourses = []
            for c in courses:
                formattedCourses.append((c.courseID, c.name))
            return render(request, "create-course.html", {"message": "Course successfully created", "courses": formattedCourses})


