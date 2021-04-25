from django.db import models

# Create your models here.


class AccountType(models.TextChoices):
    Administrator='A'
    Professor='P'
    TA='T'


class User(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=1, choices=AccountType.choices, default=AccountType.Administrator)
    phoneNumber = models.IntegerField()
    homeAddress = models.CharField(max_length=75)


class Course(models.Model):
    courseID = models.IntegerField(max_length=3)
    name = models.CharField(max_length=40)
    # TODO multiple labs
    # labs = models.ManyToManyField('Lab')
    # labList = models.ForeignKey(Lab, on_delete=models.PROTECT(), null=True)


class Instructor(User):
    coursesTaught = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)


class Administrator(User):
    title = models.CharField(max_length=40)


class TA(Instructor):
    pass


class Lab(models.Model):
    labID = models.CharField(max_length=3)
    taID = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)


class Professor(Instructor):
    pass


class Lecture(models.Model):
    profID = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True)
    taID = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)
