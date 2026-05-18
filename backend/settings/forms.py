from django import forms
from .models import UserSettings


class UserSettingsForm(forms.ModelForm):

    class Meta:

        model = UserSettings

        fields = [
            'language',
            'dark_mode',

            'email_notifications',
            'push_notifications',

            'fingerprint_login',
            'two_factor_auth',

            'autoplay_videos',
            'offline_downloads',

            'allow_chat',
            'allow_discussions',

            'live_class_reminders',
        ]

        widgets = {

            'language': forms.Select(attrs={
                'class': 'form-select'
            }),

            'dark_mode': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'push_notifications': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'fingerprint_login': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'two_factor_auth': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'autoplay_videos': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'offline_downloads': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'allow_chat': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'allow_discussions': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),

            'live_class_reminders': forms.CheckboxInput(attrs={
                'class': 'toggle'
            }),
        }