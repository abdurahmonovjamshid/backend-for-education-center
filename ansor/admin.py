from django.contrib import admin
from .models import Course, Applicant, CustomUser, Group, Student, Teacher

admin.site.register([Course, Applicant, CustomUser, Group, Student, Teacher])
