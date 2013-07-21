from django.contrib import admin

from .models import Organizer


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'added', 'post_publicly',)
    list_filter = ('added', 'post_publicly',)
    readonly_fields = ('content_object',)
    search_fields = ('name', 'email',)


admin.site.register(Organizer, OrganizerAdmin)
