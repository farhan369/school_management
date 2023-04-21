from django.contrib import admin
from . import models as academics_models


# Register your models here.

admin.site.register(academics_models.Classroom)
admin.site.register(academics_models.Exam)
admin.site.register(academics_models.Question)
admin.site.register(academics_models.Response)
admin.site.register(academics_models.AcademicYear)
admin.site.register(academics_models.Standard)
admin.site.register(academics_models.Subject)
admin.site.register(academics_models.ExamStandard)
admin.site.register(academics_models.ExamStandardSubject)
admin.site.register(academics_models.Enrollment)
admin.site.register(academics_models.Attendance)
admin.site.register(academics_models.Option)





