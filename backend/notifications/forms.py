from django import forms
from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['recipient', 'message', 'type', 'course_name', 'progress']

        widgets = {
            'recipient': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter notification message...'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Course name (optional)'
            }),
            'progress': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Progress % (optional)'
            }),
        }