from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('is_exec',)
    fieldsets = UserAdmin.fieldsets + (
        ('Executive Status', {'fields': ('is_exec',)}),
    )

admin.site.register(User, CustomUserAdmin)