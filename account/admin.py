from django.contrib import admin
from .models import Account, Student, Teacher
from rest_framework.authtoken.admin import TokenAdmin


# Register your models here.


admin.site.register(Account)
admin.site.register(Student)
admin.site.register(Teacher)

TokenAdmin.raw_id_fields = ["user"]
