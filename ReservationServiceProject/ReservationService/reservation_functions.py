import ast

from ReservationService.models import ClassName, ClassroomReservation, ClassroomReservationAttempts, ReservationDate


def get_fitting_classes(class_size=None, class_type=None):
    result_set_of_classes = ClassName.objects.all()
    if class_size:
        result_set_of_classes = result_set_of_classes.exclude(class_size__lt=class_size)
    if class_type:
        result_set_of_classes = result_set_of_classes.filter(class_type=class_type)
    return result_set_of_classes


def get_unavailable_classes(form_request: dict):
    form_request.pop('csrfmiddlewaretoken')
    form_request = {key: val for key, val in form_request.items() if val}
    date_of_class = form_request.pop('date_of_class')

    occupied_reservations = ReservationDate.objects.filter(date=date_of_class).values_list('reservation', flat=True)
    start_of_booking = form_request.pop('start_of_booking')
    end_of_booking = form_request.pop('end_of_booking')
    unavailable_classes = ClassroomReservation.objects.filter(id__in=occupied_reservations)\
        .filter(**form_request, time_start__gte=start_of_booking, time_end__lte=end_of_booking)

    return unavailable_classes.values_list('class_name', flat=True).distinct()


def get_available_classes(form_request: dict):
    class_size = form_request.pop('seats')
    class_type = form_request.pop('class_type')
    classes = get_fitting_classes(class_size, class_type)
    unavailable_classes = get_unavailable_classes(form_request)

    if form_request['class_name']:
        return [] if unavailable_classes else classes.filter(id=form_request['class_name'])
    return classes.exclude(id__in=list(unavailable_classes))


def create_reservation_attempt(form_request: dict, user):
    form_request.pop('csrfmiddlewaretoken')
    additional_dictionary = ast.literal_eval(form_request['additional_data'][12:-1])

    print(additional_dictionary)
    new_reservation_attempt = ClassroomReservationAttempts(
        class_name=ClassName.objects.get(class_name=form_request['class']),
        time_start=additional_dictionary['start_of_booking'][0],
        time_end=additional_dictionary['end_of_booking'][0],
        reserved_by=user,
        academic_year='2019/2020',
        semester='summer',
        reservation_date=additional_dictionary['date_of_class'][0]
    )

    new_reservation_attempt.save()
