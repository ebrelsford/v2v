from django.contrib import admin

from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('added_by_name', 'text', 'added',)
    list_filter = ('added',)
    search_fields = ('text', 'added_by_name',)


admin.site.register(Note, NoteAdmin)
