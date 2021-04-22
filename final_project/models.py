from django.db import models

# Create your models here.

class User(models.Model):
    # userID = models.UUIDField()
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=20)
    phoneNumber = models.IntegerField()
    homeAddress = models.CharField(max_length=75)

class Administrator(models.Model):
    title = models.CharField(max_length=40)

class TA(models.Model):
    pass

class Lab(models.Model):
    labID = models.CharField(max_length=3)
    taID = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)

class Course(models.Model):
    courseID = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    # TODO multiple labs
    # labs = models.ManyToManyField('Lab')
    #labList = models.ForeignKey(Lab, on_delete=models.PROTECT(), null=True)

class Instructor(models.Model):
    coursesTaught = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

class Professor(models.Model):
    pass

class Lecture(models.Model):
    profID = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True)
    taID = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)



