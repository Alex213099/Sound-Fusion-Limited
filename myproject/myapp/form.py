from .models import Attendance
from django import forms

class AttendanceForm(forms.ModelForm):
    class Meta:
        model=Attendance
        fields=['event','overtime_hours',]

        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),  # Dropdown
            'overtime_hours': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),  # Input box
        }
