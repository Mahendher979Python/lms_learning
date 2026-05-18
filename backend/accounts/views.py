
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.models import Notification
from courses.models import Course
from .forms import (
    StudentRegisterForm,
    LoginForm,
    TrainerForm,
    StudentForm,
    AdminUserCreateForm,
    ForgotPasswordForm,
    OTPVerifyForm,
    ResetPasswordForm
)
from .models import User, OTP
from django.db.models import Q


def view_demo(request):
    return render(request, "accounts/demo.html")


def index(request):
    return render(request, 'accounts/index.html')

def terms_view(request):
    return render(request, 'accounts/terms.html')


def register_view(request):
    form = StudentRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()

# admin notifications
        admins = User.objects.filter(role='admin')

        for admin in admins:

            Notification.objects.create(

                recipient=admin,

                sender=user,

                type='admin',

                message=f'New student registered: {user.username}'

            )
        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username_or_email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        user = None
        
        try:
            user = User.objects.get(email=username_or_email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = authenticate(request, username=username_or_email, password=password)

        if user:
            login(request, user)

            role_redirects = {
                'admin': 'admin_dashboard',
                'trainer': 'trainer_dashboard',
                'student': 'student_dashboard'
            }

            return redirect(role_redirects.get(user.role, 'login'))

    return render(request, 'accounts/login.html', {
        'form': form,
        'error': 'Invalid username or password'
    })


def is_admin(user):
    return user.role == 'admin'


@login_required
def manage_users(request):
    if not is_admin(request.user):
        return redirect('login')

    return render(request, 'accounts/manage_users.html')


@login_required
def add_user(request):
    if not is_admin(request.user):
        return redirect('login')

    form = AdminUserCreateForm(request.POST or None)

    courses = Course.objects.all()
    trainers = User.objects.filter(role='trainer')
    students = User.objects.filter(role='student')

    if form.is_valid():
        form.save()
        return redirect('view_users')

    return render(request, 'accounts/add_user.html', {
        'form': form,
        'courses': courses,
        'trainers': trainers,
        'students': students
    })


@login_required
def add_trainer(request):
    if not is_admin(request.user):
        return redirect('login')

    form = TrainerForm(request.POST or None)

    if form.is_valid():
        trainer = form.save()

        Notification.objects.create(

            recipient=trainer,

            sender=request.user,

            type='admin',

            message='Admin added you as trainer'

        )
        return redirect('view_users')

    return render(request, 'accounts/add_trainer.html', {'form': form})
@login_required
def add_student(request):

    if request.user.role != 'admin':
        return redirect('login')

    form = StudentForm(request.POST or None)

    if form.is_valid():

        # ✅ save form
        user = form.save()
        Notification.objects.create(

            recipient=user,

            sender=request.user,

            type='admin',

            message='Admin added your student account'

        )

        return redirect('view_users')

    return render(request, 'accounts/add_student.html', {
        'form': form
    })
@login_required
def view_users(request):
    if request.user.role != 'admin':
        return redirect('login')

    search = request.GET.get('search', '')
    role = request.GET.get('role')

    users = User.objects.all()

    if role in ['trainer', 'student', 'admin']:
        users = users.filter(role=role)

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    return render(request, 'accounts/view_users.html', {
        'users': users
    })

@login_required
def trainer_view(request):
    if not is_admin(request.user):
        return redirect('login')

    search = request.GET.get('search', '')

    users = User.objects.filter(role='trainer')

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    return render(request, 'accounts/trainer_view.html', {
        'users': users
    })


@login_required
def student_view(request):
    if not is_admin(request.user):
        return redirect('login')

    search = request.GET.get('search', '')

    users = User.objects.filter(role='student')

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    return render(request, 'accounts/student_view.html', {
        'users': users
    })

from courses.models import Course

@login_required
def edit_user(request, id):
    if not is_admin(request.user):
        return redirect('login')

    user = get_object_or_404(User, id=id)

    trainers = User.objects.filter(role="trainer")
    courses = Course.objects.all()   # 🔥 MUST BE HERE

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        trainer_id = request.POST.get("trainer")
        if trainer_id:
            user.trainer = User.objects.get(id=trainer_id)

        user.save()

        course_ids = request.POST.getlist("courses")
        user.courses.set(course_ids)
        Notification.objects.create(

            recipient=user,

            sender=request.user,

            type='admin',

            message='Your profile was updated by admin'

        )
        return redirect("view_users")

    return render(request, "accounts/edit_user.html", {
        "user_obj": user,
        "trainers": trainers,
        "courses": courses,   # 🔥 MUST PASS THIS
    })
    
@login_required
def delete_user(request, id):
    if not is_admin(request.user):
        return redirect('login')

    user = get_object_or_404(User, id=id)
    user.delete()
    Notification.objects.create(

            recipient=user,

            sender=request.user,

            type='admin',

            message='Your account will be removed'

        )
    return redirect('view_users')


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            otp_code = OTP.generate_otp()
            OTP.objects.filter(user=user, is_verified=False).delete()
            otp = OTP.objects.create(user=user, otp_code=otp_code)
            
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                
                subject = 'Password Reset OTP - Online Learning System'
                message = f'Hello {user.username},\n\nYour OTP for password reset is: {otp_code}\n\nThis OTP is valid for 10 minutes.\n\nIf you did not request this, please ignore this email.'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                
                send_mail(subject, message, from_email, recipient_list)
                print(f"OTP sent to {email}: {otp_code}")
            except Exception as e:
                print(f"Failed to send email: {e}")
                print(f"OTP for {email}: {otp_code}")
            
            request.session['reset_email'] = email
            return redirect('otp_verify')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'accounts/forgot_password.html', {'form': form})


def otp_verify_view(request):
    if 'reset_email' not in request.session:
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            email = request.session['reset_email']
            user = User.objects.get(email=email)
            otp_code = form.cleaned_data['otp_code']
            
            try:
                otp = OTP.objects.get(user=user, otp_code=otp_code, is_verified=False)
                
                if otp.is_expired():
                    form.add_error('otp_code', 'OTP has expired. Please request a new one.')
                    return render(request, 'accounts/otp_verify.html', {'form': form})
                
                otp.is_verified = True
                otp.save()
                
                request.session['otp_verified'] = True
                return redirect('reset_password')
                
            except OTP.DoesNotExist:
                form.add_error('otp_code', 'Invalid OTP')
    else:
        form = OTPVerifyForm()
    
    return render(request, 'accounts/otp_verify.html', {'form': form})


def reset_password_view(request):
    if 'reset_email' not in request.session or 'otp_verified' not in request.session:
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = request.session['reset_email']
            user = User.objects.get(email=email)
            
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, 'Password reset successfully! Please login.')
            return redirect('login')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'accounts/reset_password.html', {'form': form})
