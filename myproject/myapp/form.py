from django import forms
from .models import Attendance
from datetime import date

class AttendanceForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        initial=date.today()  # Automatically set today's date
    )

    class Meta:
        model = Attendance
        fields = ['event', 'overtime_hours']  # Do NOT include 'date' in fields

        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),  # Dropdown
            'overtime_hours': forms.NumberInput(attrs={'class': 'form-control', 'value': 0}),  # Input box
        }
