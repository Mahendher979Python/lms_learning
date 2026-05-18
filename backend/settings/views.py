# settings/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from django.contrib import messages

from .models import UserSettings


# =========================================
# MAIN SETTINGS PAGE
# =========================================

@login_required
def settings_page(request):

    settings_obj, created = UserSettings.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        # LANGUAGE

        language = request.POST.get("language")

        if language:

            settings_obj.language = language

            request.session["django_language"] = language

            activate(language)

        # SETTINGS

        settings_obj.dark_mode = (
            request.POST.get("dark_mode") == "on"
        )

        settings_obj.email_notifications = (
            request.POST.get("email_notifications") == "on"
        )

        settings_obj.push_notifications = (
            request.POST.get("push_notifications") == "on"
        )

        settings_obj.fingerprint_login = (
            request.POST.get("fingerprint_login") == "on"
        )

        settings_obj.two_factor_auth = (
            request.POST.get("two_factor_auth") == "on"
        )

        settings_obj.autoplay_videos = (
            request.POST.get("autoplay_videos") == "on"
        )

        settings_obj.offline_downloads = (
            request.POST.get("offline_downloads") == "on"
        )

        settings_obj.allow_chat = (
            request.POST.get("allow_chat") == "on"
        )

        settings_obj.allow_discussions = (
            request.POST.get("allow_discussions") == "on"
        )

        settings_obj.live_class_reminders = (
            request.POST.get("live_class_reminders") == "on"
        )

        settings_obj.save()

        messages.success(
            request,
            "Settings updated successfully."
        )

        return redirect("settings_page")

    return render(
        request,
        "settings/settings.html",
        {
            "settings_obj": settings_obj
        }
    )

@login_required
def admin_settings(request):
    if request.user.role != "admin":
        return redirect("login")

    user = request.user

    settings_obj, created = UserSettings.objects.get_or_create(
        user=user
    )

    if request.method == "POST":
        user.username = request.POST.get(
            "username",
            ""
        )

        user.email = request.POST.get(
            "email",
            ""
        )

        phone = (request.POST.get("phone") or "").strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            messages.error(
                request,
                "Phone number must be exactly 10 digits"
            )
            return render(
                request,
                "settings/admin_settings.html",
                {
                    "user": user,
                    "settings_obj": settings_obj,
                    "languages": UserSettings.LANGUAGE_CHOICES
                }
            )
        user.phone = phone

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get(
                "profile_image"
            )

        try:
            user.save()
        except Exception:
            messages.error(
                request,
                "Unable to save profile. Please check email/phone uniqueness."
            )
            return render(
                request,
                "settings/admin_settings.html",
                {
                    "user": user,
                    "settings_obj": settings_obj,
                    "languages": UserSettings.LANGUAGE_CHOICES
                }
            )

        language = request.POST.get(
            "language"
        )

        if language:
            settings_obj.language = language
            request.session[
                "django_language"
            ] = language
            activate(language)

        settings_obj.dark_mode = (
            request.POST.get(
                "dark_mode"
            ) == "on"
        )

        settings_obj.email_notifications = (
            request.POST.get(
                "email_notifications"
            ) == "on"
        )

        settings_obj.push_notifications = (
            request.POST.get(
                "push_notifications"
            ) == "on"
        )

        settings_obj.two_factor_auth = (
            request.POST.get(
                "two_factor_auth"
            ) == "on"
        )

        settings_obj.live_class_reminders = (
            request.POST.get(
                "live_class_reminders"
            ) == "on"
        )

        settings_obj.allow_chat = (
            request.POST.get(
                "allow_chat"
            ) == "on"
        )

        settings_obj.allow_discussions = (
            request.POST.get(
                "allow_discussions"
            ) == "on"
        )

        settings_obj.save()

        messages.success(
            request,
            "Admin profile updated successfully."
        )

        return redirect(
            "admin_settings"
        )

    return render(
        request,
        "settings/admin_settings.html",
        {
            "user": user,
            "settings_obj": settings_obj,
            "languages": UserSettings.LANGUAGE_CHOICES
        }
    )


# =========================================
# TRAINER SETTINGS
# =========================================

@login_required
def trainer_settings(request):

    if request.user.role != "trainer":
        return redirect("login")

    user = request.user

    settings_obj, created = UserSettings.objects.get_or_create(
        user=user
    )

    if request.method == "POST":

        # =====================================
        # USER DETAILS
        # =====================================

        user.username = request.POST.get(
            "username",
            ""
        )

        user.email = request.POST.get(
            "email",
            ""
        )

        user.phone = request.POST.get(
            "phone",
            ""
        )

        user.specialization = request.POST.get(
            "specialization",
            ""
        )

        user.experience = request.POST.get(
            "experience",
            ""
        )

        user.qualification = request.POST.get(
            "qualification",
            ""
        )

        user.gender = request.POST.get(
            "gender",
            ""
        )

        dob = request.POST.get("dob")

        if dob:
            user.dob = dob
        else:
            user.dob = None

        user.address = request.POST.get(
            "address",
            ""
        )

        # =====================================
        # BIO
        # =====================================

        bio = request.POST.get(
            "bio",
            ""
        ).strip()

        word_count = len(
            bio.split()
        )

        if word_count < 120 or word_count > 150:

            messages.error(
                request,
                "Professional Bio must contain 120 to 150 words only."
            )

            return render(
                request,
                "settings/trainer_settings.html",
                {
                    "user": user,
                    "settings_obj": settings_obj,
                    "languages": UserSettings.LANGUAGE_CHOICES
                }
            )

        user.bio = bio

        # =====================================
        # PROFILE IMAGE
        # =====================================

        if request.FILES.get("profile_image"):

            user.profile_image = request.FILES.get(
                "profile_image"
            )

        # =====================================
        # SAVE USER
        # =====================================

        user.save()

        # =====================================
        # LANGUAGE
        # =====================================

        language = request.POST.get(
            "language"
        )

        if language:

            settings_obj.language = language

            request.session[
                "django_language"
            ] = language

            activate(language)

        # =====================================
        # SETTINGS
        # =====================================

        settings_obj.dark_mode = (
            request.POST.get(
                "dark_mode"
            ) == "on"
        )

        settings_obj.email_notifications = (
            request.POST.get(
                "email_notifications"
            ) == "on"
        )

        settings_obj.push_notifications = (
            request.POST.get(
                "push_notifications"
            ) == "on"
        )

        settings_obj.two_factor_auth = (
            request.POST.get(
                "two_factor_auth"
            ) == "on"
        )

        settings_obj.live_class_reminders = (
            request.POST.get(
                "live_class_reminders"
            ) == "on"
        )

        settings_obj.allow_chat = (
            request.POST.get(
                "allow_chat"
            ) == "on"
        )

        settings_obj.allow_discussions = (
            request.POST.get(
                "allow_discussions"
            ) == "on"
        )

        settings_obj.save()

        messages.success(
            request,
            "Trainer profile updated successfully."
        )

        return redirect(
            "trainer_settings"
        )

    return render(
        request,
        "settings/trainer_settings.html",
        {
            "user": user,
            "settings_obj": settings_obj,
            "languages": UserSettings.LANGUAGE_CHOICES
        }
    )


# =========================================
# STUDENT SETTINGS
# =========================================

@login_required
def student_settings(request):

    if request.user.role != "student":
        return redirect("login")

    user = request.user

    settings_obj, created = UserSettings.objects.get_or_create(
        user=user
    )

    if request.method == "POST":

        # =====================================
        # USER DETAILS
        # =====================================

        user.username = request.POST.get(
            "username",
            ""
        )

        user.email = request.POST.get(
            "email",
            ""
        )

        user.phone = request.POST.get(
            "phone",
            ""
        )

        user.gender = request.POST.get(
            "gender",
            ""
        )

        dob = request.POST.get("dob")

        if dob:
            user.dob = dob
        else:
            user.dob = None

        user.address = request.POST.get(
            "address",
            ""
        )

        # =====================================
        # PROFILE IMAGE
        # =====================================

        if request.FILES.get("profile_image"):

            user.profile_image = request.FILES.get(
                "profile_image"
            )

        # =====================================
        # SAVE USER
        # =====================================

        user.save()

        # =====================================
        # LANGUAGE
        # =====================================

        language = request.POST.get(
            "language"
        )

        if language:

            settings_obj.language = language

            request.session[
                "django_language"
            ] = language

            activate(language)

        # =====================================
        # SETTINGS
        # =====================================

        settings_obj.dark_mode = (
            request.POST.get(
                "dark_mode"
            ) == "on"
        )

        settings_obj.email_notifications = (
            request.POST.get(
                "email_notifications"
            ) == "on"
        )

        settings_obj.push_notifications = (
            request.POST.get(
                "push_notifications"
            ) == "on"
        )

        settings_obj.two_factor_auth = (
            request.POST.get(
                "two_factor_auth"
            ) == "on"
        )

        settings_obj.live_class_reminders = (
            request.POST.get(
                "live_class_reminders"
            ) == "on"
        )

        settings_obj.allow_chat = (
            request.POST.get(
                "allow_chat"
            ) == "on"
        )

        settings_obj.allow_discussions = (
            request.POST.get(
                "allow_discussions"
            ) == "on"
        )

        settings_obj.save()

        messages.success(
            request,
            "Student profile updated successfully."
        )

        return redirect(
            "student_settings"
        )

    return render(
        request,
        "settings/student_settings.html",
        {
            "user": user,
            "settings_obj": settings_obj,
            "languages": UserSettings.LANGUAGE_CHOICES
        }
    )
