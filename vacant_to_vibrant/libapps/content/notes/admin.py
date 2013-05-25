from django.contrib import admin

from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('subject', 'added_by_name', 'added',)
    list_filter = ('added',)
    search_fields = ('subject', 'text', 'added_by_name',)


admin.site.register(Note, NoteAdmin)
