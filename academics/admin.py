from django.contrib import admin
from .models import Classroom,Exam,Question,Option,Response
# Register your models here.

admin.site.register(Classroom)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Option)