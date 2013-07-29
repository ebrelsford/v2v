from django.contrib import admin

from .models import PhillyDataSource


class PhillyDataSourceAdmin(admin.ModelAdmin):
    actions = ('make_healthy', 'enable', 'disable',)
    list_display = ('name', 'synchronize_in_progress', 'healthy', 'enabled',
                    'ordering', 'last_synchronized', 'next_synchronize',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'ordering',
                       'synchronizer_record',),
        }),
        ('Status', {
            'fields': (('synchronize_in_progress', 'healthy', 'enabled',),),
        }),
        ('Synchronization', {
            'fields': (
                ('last_synchronized', 'next_synchronize',
                 'synchronize_frequency',),
                'batch_size',
            ),
        }),
    )

    def make_healthy(self, request, queryset):
        queryset.update(healthy=True)
    make_healthy.short_description = "Mark selected sources as healthy"

    def enable(self, request, queryset):
        queryset.update(enabled=True)
    enable.short_description = "Enable sources"

    def disable(self, request, queryset):
        queryset.update(enabled=False)
    disable.short_description = "Disable sources"

admin.site.register(PhillyDataSource, PhillyDataSourceAdmin)
