from django.urls import path
from .views import index, register_view, login_view
from django.contrib.auth.views import LogoutView
from .views import view_demo
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('terms/', views.terms_view, name='terms'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
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
    path('users/', views.view_users, name='view_users'),
    # path('get-courses/', views.get_courses, name='get_courses')


]
