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
    courseID = models.IntegerField()
    name = models.CharField(max_length=40)


class Instructor(User):
    coursesTaught = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)


class Administrator(User):
    title = models.CharField(max_length=40)


class Professor(Instructor):
    pass


class TA(Instructor):
    skills = models.CharField(max_length=75)


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lectureID = models.IntegerField()
    profID = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True)
    taID = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sectionID = models.IntegerField()
    taID = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)
