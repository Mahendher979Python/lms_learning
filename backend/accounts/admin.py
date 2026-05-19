# from django.contrib import admin
# from .models import User

# admin.site.register(User)



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Contact


class CustomUserAdmin(UserAdmin):
    model = User

    # ❌ DO NOT add email again (already exists)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )

    list_display = ('username', 'email', 'role')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'


admin.site.register(User, CustomUserAdmin)
admin.site.register(Contact, ContactAdmin)
