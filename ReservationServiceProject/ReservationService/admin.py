from django.contrib import admin

from .models import ClassroomReservation, ClassName, ClassroomReservationAttempts, ReservationDate

# Register your models here.
admin.site.register(ClassroomReservation)
admin.site.register(ClassName)
admin.site.register(ClassroomReservationAttempts)
admin.site.register(ReservationDate)
