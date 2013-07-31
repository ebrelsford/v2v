from django.contrib import admin

from django_monitor.admin import MonitorAdmin
from livinglots_groundtruth.admin import GroundtruthRecordAdminMixin

from .models import GroundtruthRecord


class GroundtruthRecordAdmin(GroundtruthRecordAdminMixin, MonitorAdmin):
    pass


admin.site.register(GroundtruthRecord, GroundtruthRecordAdmin)
