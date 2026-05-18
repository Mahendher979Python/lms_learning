from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [

    # =========================
    # STUDENT ROUTES
    # =========================
    path("student-assignments/", views.student_assignments, name="student_assignments"),
    path("start-exam/<int:assignment_id>/", views.start_exam, name="start_exam"),
    path("submit-exam/<int:submission_id>/", views.submit_exam, name="submit_exam"),
    path("submit-pdf-exam/<int:assignment_id>/", views.submit_pdf_exam, name="submit_pdf_exam"),
    path("submit-gform-exam/<int:assignment_id>/", views.submit_gform_exam, name="submit_gform_exam"),
    path("gform-exam/<int:assignment_id>/", views.gform_exam, name="gform_exam"),  # ✅ ADD THIS
    path("exam-result/<int:submission_id>/", views.exam_result, name="exam_result"),
    path("certificate/<int:submission_id>/", views.certificate, name="certificate"),


    # =========================
    # TRAINER ROUTES
    # =========================
    path("trainer-assignments/", views.trainer_assignments, name="trainer_assignments"),
    path("trainer-create-assignment/", views.trainer_create_assignment, name="trainer_create_assignment"),
    path("trainer-submissions/<int:assignment_id>/", views.trainer_submissions, name="trainer_submissions"),
    path("grade-submission/<int:submission_id>/", views.trainer_grade_submission, name="trainer_grade_submission"),
    path("add-question/<int:assignment_id>/", views.add_question, name="add_question"),

    # 📊 GLOBAL EXPORTS (New Consolidated Routes)
    # This matches the "Export All Assignments" button in the My Assignments section.
    path("export-all-assignments/", views.export_all_assignments, name="export_all_assignments"),
    
    # This matches the "Export All Progress" button in the Student Progress section.
    path("export-all-progress/", views.export_all_progress, name="export_all_progress"),

    # Keep this for individual assignment reports if needed
    path("export-trainer-report/<int:assignment_id>/", views.export_trainer_report, name="trainer_export"),


    # =========================
    # ADMIN ROUTES
    # =========================
    path("admin-assignments/", views.admin_assignments, name="admin_assignments"),
    path("approve/<int:pk>/", views.approve_assignment, name="approve_assignment"),
    path("reject/<int:pk>/", views.reject_assignment, name="reject_assignment"),
    path('admin-create/', views.admin_create_assignment, name='admin_create_assignment'),
    path("admin-view-results/<int:assignment_id>/", views.admin_view_results, name="admin_view_results"),    # 📥 Admin global export (Total system-wide data)
    path("admin-export/", views.admin_export, name="admin_export"),
]