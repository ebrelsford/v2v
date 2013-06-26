from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from .models import Violation, ViolationType


class ViolationAdmin(CompareVersionAdmin):
    list_display = ('external_id', 'violation_type', 'violation_datetime',)
    readonly_fields = ('location', 'violation_type',)
    search_fields = ('external_id', 'location__address',)


class ViolationTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'li_description',)


admin.site.register(Violation, ViolationAdmin)
admin.site.register(ViolationType, ViolationTypeAdmin)
