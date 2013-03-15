from django.contrib import admin

from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('subject', 'added',)
    list_filter = ('added',)
    search_fields = ('subject', 'text',)


admin.site.register(Note, NoteAdmin)
