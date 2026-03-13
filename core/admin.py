from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('role', 'status')
    fieldsets = UserAdmin.fieldsets + (
        ('Organization', {'fields': ('role', 'status')}),
    )

admin.site.register(User, CustomUserAdmin)
