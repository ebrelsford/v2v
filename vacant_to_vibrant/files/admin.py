from django.contrib import admin

from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'your_name', 'added',)
    list_filter = ('added',)
    search_fields = ('title', 'description',)


admin.site.register(File, FileAdmin)
