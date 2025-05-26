from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from tickets.models import Ticket, Category, Priority, Status
from .models import CustomUser


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

    admin.site.site_header = "Administration Console"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Save M2M fields if present
        if 'categories' in form.cleaned_data:
            form.save_m2m()


class CustomAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.admin_dashboard), name='admin-dashboard'),
        ]
        return custom_urls + urls

    def admin_dashboard(self, request):
        labels = ['Nouveau', 'En cours', 'Résolu', 'Fermé']
        data = [
            Ticket.objects.filter(status__name='Nouveau').count(),
            Ticket.objects.filter(status__name='En cours').count(),
            Ticket.objects.filter(status__name='Résolu').count(),
            Ticket.objects.filter(status__name='Fermé').count(),
        ]
        context = dict(
            self.each_context(request),
            title='Statistiques',
            labels=labels,
            data=data
        )
        return TemplateResponse(request, 'admin/custom_dashbord.html', context)



# Replace default admin site
custom_admin_site = CustomAdminSite(name='customAdmin')
# Register built-in models
custom_admin_site.register(CustomUser, UserAdmin)

# Register your app models
custom_admin_site.register(Ticket)  # Or just Ticket if no custom admin
custom_admin_site.register(Category)
custom_admin_site.register(Priority)
custom_admin_site.register(Status)