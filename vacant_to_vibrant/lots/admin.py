from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import Lot, Use


class LotAdmin(OSMGeoAdmin, admin.ModelAdmin):
    exclude = ('available_property', 'parcel',)
    list_display = ('address_line1', 'city', 'owner', 'known_use',
                    'billing_account',)
    list_filter = ('known_use',)
    readonly_fields = ('added', 'available_property_link', 'billing_account',
                       'land_use_area', 'owner', 'parcel_link', 'tax_account',
                       'violations', 'water_parcel',)

    fieldsets = (
        (None, {
            'fields': ('name', 'address_line1', 'address_line2', 'city',
                       'state_province', 'postal_code', 'known_use',),
        }),
        ('Other data', {
            'classes': ('collapse',),
            'fields': ('owner', 'billing_account', 'tax_account',
                       'parcel_link', 'land_use_area', 'violations',
                       'available_property_link', 'water_parcel', 'added',),
        }),
        ('Geography', {
            'classes': ('collapse',),
            'fields': ('centroid', 'polygon',),
        }),
    )

    def available_property_link(self, obj):
        change_url = reverse(
            'admin:availableproperties_availableproperty_change',
            args=(obj.available_property.pk,)
        )
        return mark_safe('<a href="%s">%s</a>' % (change_url,
                                                  str(obj.available_property)))
    available_property_link.short_description = 'public available property record'

    def parcel_link(self, obj):
        change_url = reverse(
            'admin:parcels_parcel_change',
            args=(obj.parcel.pk,)
        )
        return mark_safe('<a href="%s">%s</a>' % (change_url, str(obj.parcel)))
    parcel_link.short_description = 'parcel'


class UseAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Lot, LotAdmin)
admin.site.register(Use, UseAdmin)
