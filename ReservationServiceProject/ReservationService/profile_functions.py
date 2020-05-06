from ReservationService.models import ClassroomReservation, ClassroomReservationAttempts


def get_my_reservations(user):
    return ClassroomReservation.objects.filter(reserved_by=user)


def get_my_waiting_reservations(user):
    return ClassroomReservationAttempts.objects.filter(reserved_by=user)


def delete_waiting_reservation(record_id):
    ClassroomReservationAttempts.objects.filter(id=record_id).delete()
