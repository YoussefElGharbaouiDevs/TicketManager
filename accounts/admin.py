from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from tickets.models import Category  # Make sure Category is imported
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone', 'profile_picture', 'categories'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions'
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'role', 'password1', 'password2', 'profile_picture', 'categories'
            ),
        }),
    )

    filter_horizontal = ('categories', 'groups', 'user_permissions')

    search_fields = ('username', 'email')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Save M2M fields if present
        if 'categories' in form.cleaned_data:
            form.save_m2m()
