
from courses.models import Course
from django import forms
from django.core.validators import RegexValidator
from .models import User, OTP, Contact
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField

class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        required=True,
        max_length=10,
        min_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Enter a valid 10-digit phone number"
            )
        ],
        widget=forms.TextInput(attrs={
            "maxlength": "10",
            "pattern": "[0-9]{10}",
            "inputmode": "numeric",
            "autocomplete": "tel",
            "oninput": "this.value=this.value.replace(/[^0-9]/g,'').slice(0,10)"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # 🔴 prevent duplicate email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        return email

    def clean_phone(self):
        phone = (self.cleaned_data.get("phone") or "").strip()
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        user.email = self.cleaned_data['email']  # ✅ ensure saved

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Username/Email")
    password = forms.CharField(widget=forms.PasswordInput)


class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'role', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user


class TrainerForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    # ✅ ADD THIS
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='student'),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'phone',
            'password',
            'courses',
            'students'
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = 'trainer'

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:

            user.save()

            self.save_m2m()

            # ✅ ASSIGN COURSES
            selected_courses = self.cleaned_data.get('courses')

            if selected_courses:

                user.courses.set(selected_courses)

                for course in selected_courses:
                    course.trainer = user
                    course.save()

            # ✅ ASSIGN STUDENTS
            selected_students = self.cleaned_data.get('students')

            if selected_students:

                for student in selected_students:
                    student.trainer = user
                    student.save()

        return user
class StudentForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'phone',
            'password',
            'trainer',
            'courses'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['trainer'].queryset = User.objects.filter(
            role='trainer'
        )

        self.fields['courses'].queryset = Course.objects.all()

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = 'student'

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:

            user.save()

            self.save_m2m()

            selected_courses = self.cleaned_data.get('courses')

            if selected_courses:

                for course in selected_courses:
                    course.students.add(user)

        return user


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email")
        return email


class OTPVerifyForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        label="OTP Code",
        widget=forms.TextInput(attrs={
            "maxlength": "6",
            "pattern": "[0-9]{6}",
            "inputmode": "numeric"
        })
    )


class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'John Doe',
                'id': 'contactName'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'john@example.com',
                'id': 'contactEmail'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'e.g. Course access query',
                'id': 'contactSubject'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Type your detailed message here...',
                'id': 'contactMessage',
                'rows': 5
            })
        }
