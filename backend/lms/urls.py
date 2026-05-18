from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # LANGUAGE URLS
    path('i18n/', include('django.conf.urls.i18n')),

]


urlpatterns += i18n_patterns(

    path('admin/', admin.site.urls),

    # ACCOUNTS
    path('', include('accounts.urls')),

    # CAPTCHA
    path('captcha/', include('captcha.urls')),

    # DASHBOARD
    path('', include('dashboard.urls')),

    # CERTIFICATES
    path('certificates/', include('certificates.urls')),

    # COURSES
    path('courses/', include('courses.urls')),

    # ASSIGNMENTS
    path('assignments/', include('assignments.urls')),

    # PROGRESS
    path('progress/', include('progress.urls')),

    # NOTIFICATIONS
    path('notifications/', include('notifications.urls')),

    # ENROLLMENTS
    path('enrollments/', include('enrollments.urls')),

    # TEAMS
    path('teams/', include('teams.urls')),

    # ATTENDANCE
    path('attendance/', include('attendance.urls')),

    # AI CHAT
    path('ai-chat/', include('ai_chat.urls')),

    # SETTINGS
    path('settings/', include('settings.urls')),
    path('coding-tasks/', include('coding_tasks.urls')),

)

# MEDIA & STATIC FILES
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )