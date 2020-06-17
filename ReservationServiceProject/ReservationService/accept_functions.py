from datetime import datetime

from django.contrib.auth.models import User

from ReservationService.models import \
    ClassroomReservationAttempts, ClassroomReservation, \
    ReservationDate, ClassName


def get_reservations_attempts():
    return ClassroomReservationAttempts.objects.all()


def get_attempt_object(object_id):
    return ClassroomReservationAttempts.objects.get(id=object_id)


def check_if_still_available(object_id):
    reservation = ClassroomReservationAttempts.objects.filter(id=object_id)
    if not reservation:
        return None
    reservation = reservation[0]
    classes_this_day = ReservationDate.objects. \
        filter(date=reservation.reservation_date).values_list('reservation', flat=True)
    any_already_reserved = ClassroomReservation.objects.filter(
        class_name=reservation.class_name,
        id__in=classes_this_day,
        time_start__gte=reservation.time_start,
        time_end__lte=reservation.time_end,
    )

    return any_already_reserved[0] if any_already_reserved else None


def add_attempt_to_reservation(object_id):
    reservation = ClassroomReservationAttempts.objects.get(id=object_id)

    new_reservation = ClassroomReservation.objects.get_or_create(
        class_name=reservation.class_name,
        time_start=reservation.time_start,
        time_end=reservation.time_end,
        is_regular=False,
        is_AB=False,
        reserved_by=reservation.reserved_by,
        academic_year=reservation.academic_year,
        semester=reservation.semester
    )

    ReservationDate.objects.get_or_create(
        reservation=new_reservation[0],
        date=reservation.reservation_date
    )
    reservation.delete()


def filter_attempts(begin_date, end_date, reserved_by):
    all_attempts = ClassroomReservationAttempts.objects.all()
    if begin_date:
        all_attempts = all_attempts.filter(reservation_date__gte=begin_date)
    if end_date:
        all_attempts = all_attempts.filter(reservation_date__lte=end_date)
    if reserved_by:
        user = User.objects.get(id=reserved_by)
        all_attempts = all_attempts.filter(reserved_by=user)
    return all_attempts


def check_if_overlap(
        attempt1: ClassroomReservationAttempts,
        attempt2: ClassroomReservationAttempts):
    if attempt1 == attempt2:
        return False
    if (attempt1.class_name == attempt2.class_name
            and attempt1.reservation_date == attempt2.reservation_date):
        if attempt1.time_start <= attempt2.time_start and attempt1.time_end >= attempt2.time_end:
            return True
        if attempt1.time_start >= attempt2.time_start and attempt1.time_end <= attempt2.time_end:
            return True
    return False


def convert_to_time_field(time):
    add_12_hours = True if time[-4:] == 'p.m.' else False
    time = time[:-4]
    time = time.split(':')
    hours = str(int(time[0]) + add_12_hours)
    minutes = time[1] if len(time) == 2 else '00'
    return hours + ':' + minutes


def process_request(request):

    if 'attempt' in request.POST:
        reserved = check_if_still_available(request.POST['attempt']), request.POST['attempt']
        if not reserved[0]:
            add_attempt_to_reservation(request.POST['attempt'])
        else:
            print("Is already reserved by:", reserved)
    elif 'OK' in request.POST:
        print("OK")
    elif 'SWAP' in request.POST:
        print("SWAP")
        reservation_attempt_id = request.POST['data'].strip('()').split(',')[1][2:-1]
        reserved = check_if_still_available(reservation_attempt_id)
        if reserved:
            reserved.delete()
        add_attempt_to_reservation(reservation_attempt_id)
    elif 'REMOVE' in request.POST:
        print("REMOVE")
        reservation_attempt_id = request.POST['data'].strip('()').split(',')[1][2:-1]
        attempt = ClassroomReservationAttempts.objects.get(id=reservation_attempt_id)
        attempt.delete()
    elif 'collisions' in request.POST:
        user, time_start, time_end = request.POST['collisions'].split(';')
        class_name, date = request.POST['collision_button'].split(';')
        # print(user, time_start, time_end, class_name, date)
        accepted_reservation = ClassroomReservationAttempts.objects.filter(
            reserved_by=user,
            time_start=convert_to_time_field(time_start),
            time_end=convert_to_time_field(time_end),
            class_name=ClassName.objects.get(class_name=class_name),
            reservation_date=datetime.strptime(date, '%B %d, %Y').date()
        ).first()
        print(accepted_reservation.id)
        overlapping_terms = ClassroomReservationAttempts.objects.filter(
            class_name=accepted_reservation.class_name,
            reservation_date=accepted_reservation.reservation_date,
            time_start__lte=accepted_reservation.time_end,
            time_end__gte=accepted_reservation.time_start,
        )
        print(overlapping_terms)
        add_attempt_to_reservation(accepted_reservation.id)
        overlapping_terms.delete()

    if 'search' in request.POST:
        attempts = filter_attempts(request.POST['begin_date'], request.POST['end_date'],
                                   request.POST['reserved_by'])
    else:
        attempts = get_reservations_attempts()

    overlapping = {}
    taken = [False] * len(attempts)

    for i in range(len(attempts)):
        if taken[i]:
            continue
        for j in range(i + 1, len(attempts)):
            if check_if_overlap(attempts[i], attempts[j]):
                if attempts[i] not in overlapping:
                    overlapping[attempts[i]] = [attempts[i]]
                overlapping[attempts[i]].append(attempts[j])
                taken[j] = True

    for base in overlapping.keys():
        for overlap in overlapping[base]:
            attempts = attempts.exclude(id=overlap.id)

    return attempts, overlapping
