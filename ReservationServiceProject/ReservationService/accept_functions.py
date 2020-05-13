from ReservationService.models import ClassroomReservationAttempts, ClassroomReservation


def get_reservations_attempts():
    return ClassroomReservationAttempts.objects.all()


def get_attempt_object(object_id):
    return ClassroomReservationAttempts.objects.get(id=object_id)


def add_attempt_to_reservation(object_id):
    reservation = ClassroomReservationAttempts.objects.get(id=object_id)
    # reservation.delete()
    ClassroomReservation.objects.get_or_create(
        class_name=reservation.class_name,
        time_start=reservation.time_start,
        time_end=reservation.time_end,
        is_regular=False,
        is_AB=False,
        reserved_by=reservation.reserved_by,
        academic_year=reservation.academic_year,
        semester=reservation.semester
    )
    reservation.delete()
