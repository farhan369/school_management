from django.contrib import admin
from .models import Sports_festival,Event,Event_registration,Try_result

# Register your models here.


admin.site.register(Sports_festival)
admin.site.register(Event)
admin.site.register(Event_registration)
admin.site.register(Try_result)