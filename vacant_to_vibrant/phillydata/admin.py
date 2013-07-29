from django.contrib import admin

from external_data_sync.admin import DataSourceAdmin

from .models import PhillyDataSource


class PhillyDataSourceAdmin(DataSourceAdmin):
    pass

admin.site.register(PhillyDataSource, PhillyDataSourceAdmin)
