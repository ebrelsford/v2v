from django.contrib import admin

from imagekit.admin import AdminThumbnail

from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')
    list_display = ('name', 'admin_thumbnail', 'added',)
    list_filter = ('added',)
    search_fields = ('name',)


admin.site.register(Photo, PhotoAdmin)
