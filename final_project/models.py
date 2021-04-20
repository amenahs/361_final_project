from django.db import models

# Create your models here.

class User(models.Model):
    # userID = models.UUIDField()
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=20)
    phoneNumber = models.IntegerField()
    homeAddress = models.CharField(max_length=75)

    # def __getPublicInfo__(self):
    #     pass
    #
    # def __editContactInfo__(self):
    #     pass
    #
    # def __sendNotification__(self):
    #     pass

# class Accounts(models.Model):
#     def __createAccount__(self):
#         pass
#
#     def __deleteAccount__(self):
#         pass
#
#     def __editAccount__(self):
#         pass

# class Assign(models.Model):
#     def __assignProfessor__(self):
#         pass
#
#     def __assignTACourse__(self):
#         pass
#
#     def __assignTALab__(self):
#         pass
"""
class Administrator(models.Model):
    title = models.CharField(max_length=40)

    def __createCourse__(self):
        pass

    def __accessData__(self):
        pass

class Lab(models.Model):
    labID = models.CharField(max_length=3)
    taID = models.ForeignKey(TA, on_delete=models.PROTECT, null=True)

class Course(models.Model):
    courseID = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    # TODO multiple labs
    labList = models.ForeignKey(Lab, on_delete=models.PROTECT(), null=True)

class Instructor(models.Model):
    coursesTaught = models.ForeignKey(Course, on_delete=models.PROTECT(), null=True)
    availability = models.CharField() # TODO convert to list

    def __viewTAs__(self):
        pass

class Professor(models.Model):
    def __assignTALab__(self):
        pass

    def __viewCourses__(self):
        pass

    def __sendTAsNotification__(self):
        pass

class TA(models.Model):
    pass

class Lecture(models.Model):
    profID = models.ForeignKey(Professor, on_delete=models.PROTECT(), null=True)
"""



