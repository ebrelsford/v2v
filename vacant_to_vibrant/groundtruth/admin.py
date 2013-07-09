from django.contrib import admin

from django_monitor.admin import MonitorAdmin

from .models import GroundtruthRecord


class GroundtruthRecordAdmin(MonitorAdmin):
    fields = ('groundtruth_target', 'actual_use', 'contact_name',
              'contact_email', 'contact_phone', 'added',)
    list_display = ('pk', 'groundtruth_target', 'actual_use', 'contact_name',
                    'contact_email', 'contact_phone', 'added',)
    readonly_fields = ('added', 'groundtruth_target',)

    def groundtruth_target(self, obj):
        try:
            return '<a href="%s" target="_blank">%s</a>' % (
                obj.content_object.get_absolute_url(),
                obj.content_object
            )
        except Exception:
            return ''
    groundtruth_target.allow_tags = True


admin.site.register(GroundtruthRecord, GroundtruthRecordAdmin)
