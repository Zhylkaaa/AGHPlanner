from django import forms


class OccupiedSlotsForm(forms.Form):
    class_name = forms.CharField(max_length=10)
