from django.shortcuts import render, redirect
from django.views import View
from .models import User, Administrator, Instructor, Professor, TA, Course
from .classes.administrator import Admin
# Create your views here.

class Home(View):
    def get(self,request):
        return render(request, "home.html", {})
    def post(self,request):
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
            request.session["name"] = m.email
            return redirect("/dashboard/")

class Dashboard(View):
    pass

class CreateAccount(View):
    pass

class CreateCourse(View):
    def get(self,request):
        return render(request, "create-course.html", {})
    def post(self, request):
        newCourseID = request.POST['courseID']
        newCourseName = request.POST['name']
        try:
            a = Admin()
            a.__createCourse__(newCourseID, newCourseName)
        except ValueError:
            return render(request, "create-course.html", {"message": "course already exists"})
        except TypeError:
            return render(request, "create-course.html", {"message": "invalid input"})
        else:
            return render(request, "create-course.html", {"message": "course successfully created"})

