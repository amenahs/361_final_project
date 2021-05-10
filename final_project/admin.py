from django.contrib import admin
from .models import User, Administrator, Professor, TA, Course, Lecture, Section, TASectionAllocation

# Register your models here.
admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Professor)
admin.site.register(TA)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Section)
admin.site.register(TASectionAllocation)