from django.shortcuts import render, redirect
from django.views import View
from .models import User
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
            return render(request, "home.html", {"message": "user does not exist"})
        elif badPassword:
            return render(request, "home.html", {"message": "bad password"})
        else:
            return render(request, "home.html", {"message": "an error occurred, please try again"})