from datetime import datetime
from datetime import timedelta

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.urls import reverse

from .models import ClassroomReservation
from .forms import OccupiedSlotsForm
import pandas as pd


# Create your views here.
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


def book_slot(request):
    print(Group.objects.get(name='LA') in request.user.groups.all())
    return HttpResponse('U can book a slot here')


def _validate_and_choose_columns(classes_df):
    # dangerous method: ClassroomReservation._meta.get_fields()
    required_columns = ['class_name', 'reserved_from', 'reserved_until', 'time_start',
                        'is_AB', 'academic_year', 'semester']

    for col in required_columns:
        if col not in classes_df:
            return False, None

    return True, 'time_end' in required_columns


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

    classes_df = pd.read_csv(csv_file.name, index_col=0)
    is_valid, use_time_end = _validate_and_choose_columns(classes_df)

    if not is_valid:
        context['error_message'] = "file doesn't contain required columns"
        return render(request, template, context)

    columns = classes_df.columns

    for row in classes_df.itertuples(index=False):
        data = dict(zip(columns, row))
        if not use_time_end:
            data['time_end'] = str((datetime.strptime(data['time_start'], '%H:%M:%S') + timedelta(hours=1, minutes=30)).time())

        ClassroomReservation.objects.get_or_create(**data)

    current_year = datetime.now().year
    semester = 'winter'

    if current_year % 2 == 0:
        current_year -= 1
        semester = 'summer'

    current_year = str(current_year) + '_' + str(current_year + 1)

    return HttpResponseRedirect(reverse('ReservationService:calendar_view', args=(current_year, semester, )))


def calendar(request, academic_year, semester):
    template = 'ReservationService/calendar_view.html'

    academic_year = academic_year.replace('_', '/')

    print(academic_year, semester)
    reservation_list_for_semester = ClassroomReservation.objects.filter(academic_year=academic_year, semester=semester)

    return render(request, template, {'reservation_list': reservation_list_for_semester})
