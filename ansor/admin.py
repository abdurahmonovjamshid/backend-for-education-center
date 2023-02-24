from django.contrib import admin
from .models import Course, Applicant, CustomUser

admin.site.register([Course, Applicant, CustomUser])
