from django import forms

from ReservationService.models import ClassroomReservation, ClassTypes, ClassName
from django.contrib.auth.models import User
import datetime as dt


class OccupiedSlotsForm(forms.Form):
    class_name = forms.CharField(max_length=10)


class SpecificClassReservationFrom(forms.Form):
    class_name = forms.ModelChoiceField(queryset=ClassName.objects.all())


class DataInput(forms.DateInput):
    input_type = 'date'


class ReservationForm(forms.ModelForm):
    # class_name = forms.CharField(required=False)
    TIME_CHOICES_BEGIN = (
        (dt.time(hour=8, minute=0), "8:00"),
        (dt.time(hour=9, minute=35), "9:35"),
        (dt.time(hour=11, minute=15), "11:15"),
        (dt.time(hour=12, minute=50), "12:50"),
        (dt.time(hour=14, minute=40), "14:40"),
        (dt.time(hour=16, minute=15), "16:15")
    )
    TIME_CHOICES_END = (
        (dt.time(hour=9, minute=30), "9:30"),
        (dt.time(hour=11, minute=5), "11:05"),
        (dt.time(hour=12, minute=45), "12:45"),
        (dt.time(hour=14, minute=20), "14:20"),
        (dt.time(hour=16, minute=10), "16:10"),
        (dt.time(hour=17, minute=45), "17:45")
    )
    date_of_class = forms.DateField(widget=DataInput)
    start_of_booking = forms.ChoiceField(choices=TIME_CHOICES_BEGIN)
    end_of_booking = forms.ChoiceField(choices=TIME_CHOICES_END)
    seats = forms.IntegerField(min_value=0, max_value=1000, initial=0)
    class_type = forms.ChoiceField(choices=([(None, '--------')] + ClassTypes.choices)
                                   , initial={None, '--------'})

    class Meta:
        model = ClassroomReservation
        fields = ('class_name',)

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['class_name'].required = False
        self.fields['seats'].required = False
        self.fields['class_type'].required = False

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()
        begin = cleaned_data.get('start_of_booking')
        end = cleaned_data.get('end_of_booking')
        if begin > end:
            raise forms.ValidationError('Start time is after end time')


class ReservationFilterForm(forms.Form):
    begin_date = forms.DateField(widget=DataInput)
    end_date = forms.DateField(widget=DataInput)
    reserved_by = forms.ModelChoiceField(
        queryset=User.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(ReservationFilterForm, self).__init__(*args, **kwargs)
        self.fields['begin_date'].required = False
        self.fields['end_date'].required = False
        self.fields['reserved_by'].required = False
