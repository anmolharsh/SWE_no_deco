from django.contrib import admin

# Register your models here.
from .models import Profile, Attendence, Schedule, Leave, Complaint, Visitor, Routine, Appointment

admin.site.register(Profile)
admin.site.register(Attendence)
admin.site.register(Schedule)
admin.site.register(Leave)

admin.site.register(Complaint)
admin.site.register(Visitor)
admin.site.register(Routine)
admin.site.register(Appointment)