from ast import literal_eval
from datetime import datetime
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.urls import reverse

from .models import ClassroomReservation, ClassName, ClassTypes, ReservationDate
from .forms import OccupiedSlotsForm, ReservationForm, SpecificClassReservationFrom
import pandas as pd


# Create your views here.
from .profile_functions import get_my_reservations, get_my_waiting_reservations, delete_waiting_reservation, \
    delete_reservation
from .reservation_functions import get_available_classes, create_reservation_attempt


def home(request):
    available_semesters = list(ClassroomReservation.objects.values_list('academic_year', 'semester').distinct())
    available_semesters.sort(key=lambda x: x[0]+x[1], reverse=True)
    tmp = []

    for year, semester in available_semesters:
        if len(tmp) != 0 and tmp[-1][0] == year:
            tmp[-1][1].append(semester)
        else:
            tmp.append((year, [semester]))
    tmp = [(x.replace('/', '_'), y) for x, y in tmp]
    return render(request, "ReservationService/home.html", {'available_semesters': tmp})


@login_required
def profile_view(request):
    data_base_respond = None
    request_type = None
    print(request.POST)
    if request.POST:
        if 'reservation' in request.POST:
            request_type = 'reservation'
            data_base_respond = get_my_reservations(request.user)
            # print(data_base_respond)
        elif 'waiting' in request.POST:
            request_type = 'waiting'
            data_base_respond = get_my_waiting_reservations(request.user)
        elif 'to_delete' in request.POST:
            if request.POST['type'] == 'waiting':
                delete_waiting_reservation(request.POST['to_delete'])
                data_base_respond = get_my_waiting_reservations(request.user)
                request_type = 'waiting'
            else:
                delete_reservation(request.POST['to_delete'])
                data_base_respond = get_my_reservations(request.user)
                request_type = 'reservation'
    return render(request, "registration/profile.html", {'content': data_base_respond, 'type': request_type})


@login_required
def reservation(request):
    # print(request.POST)
    if request.POST and 'additional_data' in request.POST:
        create_reservation_attempt(request.POST.dict(), request.user)
        return render(request, "ReservationService/reservation.html", {'form': ReservationForm()})
    else:
        available_classes = ()
        form = ReservationForm(request.POST or None)
        if form.is_valid():
            form2 = SpecificClassReservationFrom()
            available_classes = get_available_classes(request.POST.dict())
            form2.fields['class_name'].choices = [(obj.class_name, obj) for obj in available_classes]
        context = {'form': form, 'available_class': available_classes}
    return render(request, "ReservationService/reservation.html", context)


def booked_slots(request):
    form = OccupiedSlotsForm(request.POST or None)
    class_name = None
    if form.is_valid():
        class_name = request.POST['class_name']

        form = OccupiedSlotsForm()

    booked_slots_of_the_class = ClassroomReservation.objects.filter(class_name=class_name)

    available_class = ClassroomReservation.objects.values_list('class_name', flat=True).distinct()

    context = {
        'all_booked_slots': booked_slots_of_the_class,
        'form': form,
        'available_class': available_class
    }
    # return HttpResponse(result)
    return render(request, "ReservationService/booked_slots.html", context)


def _validate_and_choose_columns(classes_df):
    # dangerous method: ClassroomReservation._meta.get_fields()
    required_columns = ['class_name', 'time_start', 'time_end',
                        'is_AB', 'academic_year', 'semester', 'reservations']

    for col in required_columns:
        if col not in classes_df:
            return False, None

    return True, 'time_end' in required_columns


@staff_member_required
def upload_csv(request):
    template = 'ReservationService/upload_csv.html'

    context = {
        'message': 'Upload CSV in following format: TODO',  # TODO: extract string constants to separate file
    }

    if request.method == 'GET':
        return render(request, template, context)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        context['error_message'] = 'file should have .csv extension'
        return render(request, template, context)

    classes_df = pd.read_csv(csv_file.name, index_col=0, converters={'reservations': literal_eval})
    is_valid, use_time_end = _validate_and_choose_columns(classes_df)

    if not is_valid:
        context['error_message'] = "file doesn't contain required columns"
        return render(request, template, context)

    columns = classes_df.columns

    redirect_year, redirect_semester = None, None

    for row in classes_df.itertuples(index=False):
        data = dict(zip(columns, row))
        # if not use_time_end:
        #     data['time_end'] = str((datetime.strptime(data['time_start'], '%H:%M:%S') + timedelta(hours=1, minutes=30)).time())

        # print(data)
        # print(data['reservations'][1])
        reservations = data.pop('reservations')
        redirect_year = data['academic_year']
        redirect_semester = data['semester']
        data['class_name'] = ClassName.objects.get(class_name=data['class_name'])
        reservation_object, created = ClassroomReservation.objects.get_or_create(**data)
        if created:
            for date in reservations:
                ReservationDate.objects.get_or_create(reservation=reservation_object, date=date)

    redirect_year = redirect_year.replace('/', '_')

    return HttpResponseRedirect(reverse('ReservationService:calendar_view', args=(redirect_year, redirect_semester, )))


def calendar(request, academic_year, semester):
    template = 'ReservationService/calendar_view.html'

    academic_year = academic_year.replace('_', '/')

    print(academic_year, semester)
    reservation_list_for_semester = ClassroomReservation.objects.filter(academic_year=academic_year, semester=semester)

    return render(request, template, {'reservation_list': reservation_list_for_semester})
