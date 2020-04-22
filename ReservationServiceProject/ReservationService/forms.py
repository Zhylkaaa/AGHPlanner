from django import forms


class OccupiedSlotsForm(forms.Form):
    class_number = forms.CharField(max_length=10)
