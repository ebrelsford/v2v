from django.contrib import admin

from .models import PhillyDataSource


class PhillyDataSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'healthy', 'ordering', 'last_synchronized',
                    'next_synchronize',)

admin.site.register(PhillyDataSource, PhillyDataSourceAdmin)
