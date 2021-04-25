from django.contrib import admin
from .models import User, Instructor, Administrator, Professor, TA, Course, Lecture, Lab

# Register your models here.
admin.site.register(User)
admin.site.register(Instructor)
admin.site.register(Administrator)
admin.site.register(Professor)
admin.site.register(TA)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Lab)