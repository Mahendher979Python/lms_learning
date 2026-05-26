from django.urls import path
from .views import index, register_view, login_view
from .views import view_demo
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('terms/', views.terms_view, name='terms'),
    path('terms-of-service/', views.terms_page, name='terms_page'),
    path('conditions/', views.conditions_page, name='conditions_page'),
    path('about-us/', views.about_us, name='about_us'),
    path('about/', views.about_view, name='about'),
    path('courses/', views.courses_view, name='courses'),
    path('services/', views.services_view, name='services'),
    path('faq/', views.faq_view, name='faq'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', register_view, name='register'),
    path('register/otp-verify/', views.register_otp_verify_view, name='register_otp_verify'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('demo/', view_demo, name='demo'),
    path('add-user/', views.add_user, name='add_user'),
    path('users/', views.view_users, name='view_users'),
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('add-trainer/', views.add_trainer, name='add_trainer'),
    path('trainer_view/', views.trainer_view, name='trainer_view'),
    path('student_view/', views.student_view, name='student_view'),
    path('add-student/', views.add_student, name='add_student'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    # path('get-courses/', views.get_courses, name='get_courses')


]
