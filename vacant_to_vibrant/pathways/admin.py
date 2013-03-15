from django.contrib import admin

from .models import Pathway


class PathwayAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = { "slug": ("name",) }
    search_fields = ('name',)


admin.site.register(Pathway, PathwayAdmin)
