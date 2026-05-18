from django import forms
from .models import Team
from django.contrib.auth import get_user_model

User = get_user_model()


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'trainer', 'students']

        widgets = {
            'students': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['trainer'].queryset = User.objects.filter(role='trainer')
        self.fields['students'].queryset = User.objects.filter(role='student')
