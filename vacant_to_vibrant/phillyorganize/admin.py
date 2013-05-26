from django.contrib import admin

from .models import Organizer, Watcher


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'added',)
    list_filter = ('added',)
    readonly_fields = ('content_object',)
    search_fields = ('name', 'email',)


class WatcherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'added',)
    list_filter = ('added',)
    readonly_fields = ('content_object',)
    search_fields = ('name', 'email',)


admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Watcher, WatcherAdmin)
