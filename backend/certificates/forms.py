from django import forms
from .models import Certificate


class CertificateForm(forms.ModelForm):

    class Meta:

        model = Certificate

        fields = [

            'student_photo',
            'director_signature',
            'director_name',
            'certificate_title',
            'description',
        ]

        widgets = {

            'director_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'certificate_title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),
        }