from django.contrib import admin

from models import Organizer, OrganizerType, Watcher


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'added',)
    list_filter = ('added',)
    readonly_fields = ('target',)
    search_fields = ('name', 'email',)


class OrganizerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_group',)
    search_fields = ('name',)


class WatcherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'added',)
    list_filter = ('added',)
    search_fields = ('name', 'email',)


admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(OrganizerType, OrganizerTypeAdmin)
admin.site.register(Watcher, WatcherAdmin)
