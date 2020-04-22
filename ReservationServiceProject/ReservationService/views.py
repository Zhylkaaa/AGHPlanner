from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group

from ReservationService.models import ClassroomReservation
from .forms import OccupiedSlotsForm


# Create your views here.
def booked_slots(request):
    form = OccupiedSlotsForm(request.POST or None)
    class_number = None
    if form.is_valid():
        class_number = request.POST['class_number']

        form = OccupiedSlotsForm()
    booked_slots_of_the_class = [x for x in ClassroomReservation.objects.all() if x.class_number == class_number]
    available_class = set(x.class_number for x in ClassroomReservation.objects.all())
    context = {
        'all_booked_slots': booked_slots_of_the_class,
        'form': form,
        'available_class': available_class
    }
    # return HttpResponse(result)
    return render(request, "booked_slots.html", context)


def book_slot(request):
    print(Group.objects.get(name='LA') in request.user.groups.all())
    return HttpResponse('U can book a slot here')
