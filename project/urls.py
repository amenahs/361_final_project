"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from final_project.views import Home, Dashboard, CreateAccount, CreateCourse, EditInformation, ViewInformation, \
    AssignProfCourse, AssignTACourse, AssignTASection, Error, ForgotPassword, AllocateSections, EditAccount

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path('dashboard/', Dashboard.as_view()),
    path('error-page/', Error.as_view()),
    path('create-account/', CreateAccount.as_view()),
    path('create-course/', CreateCourse.as_view()),
    path('edit-information/', EditInformation.as_view()),
    path('view-information/', ViewInformation.as_view()),
    path('assign-prof-course/', AssignProfCourse.as_view()),
    path('allocate-sections/', AllocateSections.as_view()),
    path('assign-ta-course/', AssignTACourse.as_view()),
    path('assign-ta-section/', AssignTASection.as_view()),
    path('edit-account/', EditAccount.as_view()),
    path('forgot-password/', ForgotPassword.as_view())
]
