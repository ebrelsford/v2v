from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from .models import Violation, ViolationType


class ViolationAdmin(CompareVersionAdmin):
    date_hierarchy = 'violation_datetime'
    list_display = ('external_id', 'case_number', 'violation_type',
                    'violation_datetime',)
    readonly_fields = ('external_id', 'case_number', 'location',
                       'violation_type', 'violation_datetime',)
    search_fields = ('external_id', 'case_number', 'location__address',)


class ViolationTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'li_description',)


admin.site.register(Violation, ViolationAdmin)
admin.site.register(ViolationType, ViolationTypeAdmin)
