from django.contrib import admin

from .models import ClassroomReservation, ClassName

# Register your models here.
admin.site.register(ClassroomReservation)
admin.site.register(ClassName)