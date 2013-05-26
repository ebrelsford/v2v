from django.contrib import admin

from .models import OrganizerType


class OrganizerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_group',)
    search_fields = ('name',)


admin.site.register(OrganizerType, OrganizerTypeAdmin)
