from django.contrib import admin
from .models import SportsFestival,Event,EventRegistration,Try

# Register your models here.


admin.site.register(SportsFestival)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(Try)