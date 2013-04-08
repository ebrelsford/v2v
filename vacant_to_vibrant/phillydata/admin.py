from django.contrib import admin

from .models import PhillyDataSource


class PhillyDataSourceAdmin(admin.ModelAdmin):
    actions = ('make_healthy',)
    list_display = ('name', 'healthy', 'synchronize_in_progress', 'ordering',
                    'last_synchronized', 'next_synchronize',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'ordering',),
        }),
        ('Status', {
            'fields': (('synchronize_in_progress', 'healthy', 'enabled',),),
        }),
        ('Synchronization', {
            'fields': (('last_synchronized', 'next_synchronize',
                        'synchronize_frequency',),),
        }),
    )

    def make_healthy(self, request, queryset):
        queryset.update(healthy=True)
    make_healthy.short_description = "Mark selected sources as healthy"

admin.site.register(PhillyDataSource, PhillyDataSourceAdmin)
