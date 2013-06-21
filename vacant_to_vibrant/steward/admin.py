from django.contrib import admin

from django_monitor.admin import MonitorAdmin

from .models import StewardNotification, StewardProject


class StewardNotificationAdmin(MonitorAdmin):
    list_display = ('name',)


class StewardProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizer', 'use',)


admin.site.register(StewardNotification, StewardNotificationAdmin)
admin.site.register(StewardProject, StewardProjectAdmin)
