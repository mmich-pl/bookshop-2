from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class UserAdminConfig(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('-joined_date',)

    fieldsets = (
        ('Personal Information', {'fields': ('email', 'username', 'first_name', 'last_name',)}),
        ('Account Information', {'fields': ('is_active', 'joined_date', 'last_login',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')
        })
    )


admin.site.register(CustomUser, UserAdminConfig)
