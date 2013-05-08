from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from .models import Contact, License, LicenseType


class LicenseAdmin(CompareVersionAdmin):
    list_display = ('external_id', 'location', 'license_type', 'status',)
    list_filter = ('license_type', 'status', 'issued_datetime',)
    readonly_fields = ('external_id', 'location', 'license_type',
                       'primary_contact',)
    search_fields = ('location__address', 'primary_contact__last_name',
                     'primary_contact__company_name',)
    fieldsets = (
        (None, {
            'fields': ('location', 'external_id', 'primary_contact',
                       'license_type', 'status',),
        }),
        ('Dates', {
            'fields': (
                ('issued_datetime', 'inactive_datetime',),
                ('expires_month', 'expires_year',),
            ),
        }),
    )


class LicenseTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('address1', 'city', 'contact_type', 'company_name',
                    'first_name', 'last_name',)


admin.site.register(Contact, ContactAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(LicenseType, LicenseTypeAdmin)
