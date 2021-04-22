from django.shortcuts import render, redirect
from django.views import View
from .models import User, Administrator, Instructor, Professor, TA, Course
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
            return render(request, "home.html", {"message":"an error occurred, please try again"})

class Dashboard(View):
    pass

class CreateAccount(View):
    pass

class CreateCourse(View):
    def get(self,request):
        return render(request, "create-course.html", {})
    def post(self, request):
        courseExists = False
        try:
            c = Course.objects.get(courseID=request.POST['courseID'])
            courseExists = True
        except:
            newCourse = Course.objects.create(courseID=request.POST['courseID'], name=request.POST['name'])
            newCourse.save()

        if courseExists:
            return render(request, "create-course.html", {"message": "course already exists"})
        else:
            return render(request, "create-course.html", {"message": "course successfully created"})

