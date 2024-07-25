from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email', 'date_of_birth', 'age', 'gender', 'city', 'state', 'public_visibility')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'password1', 'password2'),
        }),
    )

    list_display = ('id', 'username', 'email', 'full_name', 'is_staff', 'is_active', 'public_visibility')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'description', 'visibility', 'cost', 'year_published', 'file']
