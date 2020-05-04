from django import forms

from ReservationService.models import ClassroomReservation


class OccupiedSlotsForm(forms.Form):
    class_name = forms.CharField(max_length=10)


class ReservationForm(forms.ModelForm):
    # class_name = forms.CharField(required=False)
    TIME_CHOICES_BEGIN = (
        ("1", "8:00"),
        ("2", "9:35"),
        ("3", "11:15"),
        ("4", "12:50"),
        ("5", "14:40"),
        ("6", "16:15")
    )
    TIME_CHOICES_END = (
        ("1", "9:30"),
        ("2", "11:05"),
        ("3", "12:45"),
        ("4", "14:20"),
        ("5", "16:10"),
        ("6", "17:45")
    )
    start_of_booking = forms.ChoiceField(choices=TIME_CHOICES_BEGIN)
    end_of_booking = forms.ChoiceField(choices=TIME_CHOICES_END)

    class Meta:
        model = ClassroomReservation
        fields = ('class_name', )

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['class_name'].required = False
